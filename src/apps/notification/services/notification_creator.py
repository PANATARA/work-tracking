from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, List, Union
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from core.services.baseservice import BaseService, GetObjectsByIdService
from apps.notification.models.notification import Notification
from apps.users.models.users import User
from apps.workspace.models.workspace import Workspace


@dataclass
class NotificationCreatorService(BaseService, GetObjectsByIdService):
    """Service responsible for creating notifications:

    - User added to task assignees
    - Task reminder for the user from the manager
    - Notification for all participants in the Workspace
    """

    users: list[User | int]  # Users to whom notification should be sent
    workspace: Workspace | int
    notification_type: int
    triggered_by: User | int | None  # The user who triggered the notification
    message: str | None
    entity_type: str | None
    entity_identifier: int | None

    def __post_init__(self):
        self.load_objects()

    def execute(self) -> Any:
        notifications = self.get_notification_objects()
        self.bulk_create_notifications(notifications)

    def get_notification_objects(self) -> List[Notification]:
        common_data = {
            "workspace": self.workspace,
            "type": self.notification_type,
            "triggered_by": self.triggered_by,
            "message": self.message,
            "entity_type": self.entity_type,
            "entity_identifier": self.entity_identifier,
            "created_at": timezone.now(),
        }
        return [Notification(user=user, **common_data) for user in self.users]

    def bulk_create_notifications(self, notifications: List[Notification]) -> None:
        Notification.objects.bulk_create(notifications)

    def get_validators(self) -> List[Callable[..., Any]]:
        return [self.validate_entity_object]

    def validate_entity_object(self) -> None:
        """Checking the existence of an entity object"""
        from core.constants import get_entity_model
        if self.entity_identifier and self.entity_type:
            entity_model = get_entity_model(self.entity_type)
            if entity_model and not entity_model.objects.filter(pk=self.entity_identifier).exists():
                raise ValidationError(f"Object {entity_model} does not exist")


@dataclass
class TaskAssigneesNotificationService(NotificationCreatorService):

    def get_validators(self) -> List[Callable[..., Any]]:
        return super().get_validators() + [self.validate_user_mention_preferences]

    def validate_user_mention_preferences(self) -> None:
        self.users = [user for user in self.users if user.settings.mention]
