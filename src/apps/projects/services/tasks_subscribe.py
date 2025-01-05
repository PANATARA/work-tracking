from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from django.core.exceptions import ValidationError

from core.services.baseservice import (
    BaseService,
    GetObjectsByIdService,
)
from apps.projects.models.tasks import Task, TaskSubscriber
from apps.workspace.validators import all_user_in_workspace
from apps.users.models.users import User


@dataclass
class SubscribeUserToTaskService(GetObjectsByIdService, BaseService):
    task: Task | int
    users: list[User | int]

    def __post_init__(self):
        self.users = list(set(self.users))
        self.load_objects()

    def execute(self) -> Any:
        data = self.get_task_subscriber_objects()
        self.create_task_subscriber(data)

    def get_task_subscriber_objects(self) -> list[TaskSubscriber]:
        common_data = {"task": self.task, "workspace": self.task.workspace}
        return [TaskSubscriber(subscriber=user, **common_data) for user in self.users]

    @staticmethod
    def create_task_subscriber(subscribers: list[TaskSubscriber]) -> None:
        TaskSubscriber.objects.bulk_create(subscribers)

    def get_validators(self) -> list[Callable[..., Any]]:
        return [self.validate_users]

    def validate_users(self):
        if not all_user_in_workspace(self.users, self.task.workspace):
            raise ValidationError("Not all users were found in this workspace")
        self.users = list(
            [
                user
                for user in self.users
                if user.settings.auto_subsсribe_to_task
                and not TaskSubscriber.objects.filter(
                    subscriber=user, task=self.task
                ).exists()
            ]
        )
    
    @staticmethod
    def list_users_to_get_notify(task: Task) -> list[int]:
        return list(
            TaskSubscriber.objects.filter(
            task=task
            ).values_list(
                "subscriber_id", 
                flat=True
            )
        )

@dataclass
class UnsubscribeUserToTaskService(GetObjectsByIdService, BaseService):
    task: Task | int
    users: list[User | int]

    def __post_init__(self):
        self.users = list(set(self.users))
        self.load_objects()

    def execute(self) -> Any:
        self.delete_task_subscription(self.users, self.task)

    @staticmethod
    def delete_task_subscription(users: list, task):
        TaskSubscriber.objects.filter(task=task, subscriber__in=users).delete()

    def get_validators(self) -> list[Callable[..., Any]]:
        return [self.validate_users]

    def validate_users(self):
        self.users = list([user for user in self.users if user != self.task.created_by])