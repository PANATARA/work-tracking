from abc import abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from django.db import transaction
from crum import get_current_user
from rest_framework.exceptions import ValidationError

from core.services.baseservice import BaseService, GetObjectsByIdService
from apps.notification.celery_tasks import send_notification
from apps.projects.models.tasks import TaskSubscriber
from apps.workspace.constant import RoleChoices
from apps.workspace.models.workspace import Workspace, WorkspaceMember
from apps.users.models.users import User
from apps.workspace.models.workspace_user_config import UserWorkspaceConfig
from apps.workspace.services.workspace_user_config import UserWorkspaceConfigCreator
from apps.workspace.validators import all_user_in_workspace


@dataclass
class WorkspaceMemberService(BaseService):
    """
    Service for adding users to the workspace

    Functionality:

    - Adds users to the workspace with a role
    - Creates a User Workspace Config
    """

    workspace: Workspace
    users_roles: list[dict[User, int]]

    def execute(self) -> Any:
        self.workspace_set_members_with_roles()

    def workspace_set_members_with_roles(self) -> None:
        for user_data in self.users_roles:

            user = user_data["user"]
            role = user_data.get("role", RoleChoices.MEMBER)

            if not WorkspaceMember.objects.filter(workspace=self.workspace, user=user).exists():
                self.workspace_member_create(self.workspace, user, role)
            else:
                self.member_update_role(self.workspace, user, role)

    @staticmethod
    def workspace_member_create(workspace, user, role):
        """
        - Adds a user to a workspace 
        - Creates a configuration for that workspace
        """
        WorkspaceMember.objects.create(
            workspace=workspace, 
            user=user, 
            role=role
        )
        UserWorkspaceConfigCreator(user, workspace)()
    
    @staticmethod
    def member_update_role(workspace, user, new_role):
        """
        - Updates a member's role
        - Sends a role update notification
        """
        WorkspaceMember.objects.filter(
            workspace=workspace, 
            user=user
        ).update(
            role=new_role
        )
        notification_data = {
            "users_ids": [user.id],
            "workspace_id": workspace.id,
            "notification_type": 1,
            "triggered_by":None,
            "message": f"You have been assigned a new role: '{new_role}' in the workspace: '{workspace.name}'",
            "entity_type":"workspace",
            "entity_identifier":workspace.id,
        }
        send_notification.delay(**notification_data)


@dataclass
class BaseMemberExitService(BaseService, GetObjectsByIdService):
    """Base class for implementing workspace exit

    - For all projects where the user is a manager, the manager value is set to NULL
    - The user is removed from the assignees field for all tasks associated with him
    - All user settings in this Workspace are deleted
    """

    user: User | int
    workspace: Workspace | int

    def __post_init__(self):
        self.current_user = get_current_user()
        self.load_objects()

    def execute(self) -> Any:
        with transaction.atomic():
            self.delete_users_subscribers()
            self.remove_from_task_assignees()
            self.remove_from_project_management()
            self.delete_user_workspace_config()
            self.remove_user_from_workspace()
        data = self.get_data_for_notification()
        from apps.notification.celery_tasks import send_notification

        send_notification.delay(**data)
        return

    def remove_from_project_management(self) -> None:
        self.user.managed_projects.filter(workspace=self.workspace).update(manager=None)

    def remove_from_task_assignees(self) -> None:
        tasks = self.user.assigned_tasks.filter(workspace=self.workspace)
        for task in tasks:
            task.assignees.remove(self.user)

    def delete_users_subscribers(self):
        TaskSubscriber.objects.filter(
            subscriber=self.user, workspace=self.workspace
        ).delete()

    def delete_user_workspace_config(self) -> None:
        UserWorkspaceConfig.objects.filter(
            user=self.user, workspace=self.workspace
        ).delete()

    def remove_user_from_workspace(self):
        workspace_member = WorkspaceMember.objects.get(
            workspace=self.workspace, user=self.user
        )
        self.ex_member_data = {
            "role": workspace_member.role,
            "date_joined": workspace_member.date_joined,
        }
        workspace_member.delete()

    @abstractmethod
    def get_data_for_notification(self) -> dict:
        return {}

    def get_validators(self) -> list[Callable[..., Any]]:
        return [
            self.validate_user_workspace,
        ]

    def validate_user_workspace(self):
        if not all_user_in_workspace([self.user], self.workspace):
            raise ValidationError("No such user in this workspace")


class MemberKickService(BaseMemberExitService):
    """Kick a member from apps.workspace

    - The kicked user receives a notification

    """

    def get_data_for_notification(self) -> dict:
        return {
            "users_ids": [self.user.id],
            "workspace_id": self.workspace.id,
            "notification_type": 2,
            "triggered_by": self.current_user.id,
            "message": f"You have been kicked from apps.workspace {self.workspace.name}",
        }

    def get_validators(self) -> list[Callable[..., Any]]:
        return super().get_validators() + [self.vallidate_user_legal]

    def vallidate_user_legal(self):
        current_user_role = WorkspaceMember.objects.get(
            user=self.current_user, workspace=self.workspace
        ).role
        user_role = WorkspaceMember.objects.get(
            user=self.user, workspace=self.workspace
        ).role
        if user_role >= current_user_role:
            raise ValidationError("You dont have permissions")


class MemberLogoutService(BaseMemberExitService):
    """Leaving a participant from apps.workspace

    - All Workspace admins receive a notification that the user has logged out

    """

    def get_data_for_notification(self) -> dict:
        workspace_management_ids = list(
            WorkspaceMember.objects.filter(
                workspace=self.workspace, role__gte=RoleChoices.ADMIN
            ).values_list("user", flat=True)
        )

        return {
            "users_ids": workspace_management_ids,
            "workspace_id": self.workspace.id,
            "notification_type": 2,
            "triggered_by": self.user.id,
            "message": f"User {self.user.username} has left",
        }

    def get_validators(self) -> list[Callable[..., Any]]:
        return super().get_validators() + [self.validate_user_is_not_owner]

    def validate_user_is_not_owner(self):
        if self.workspace.owner == self.user:
            raise ValidationError("The workspace owner can't log out")
