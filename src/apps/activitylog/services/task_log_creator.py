from dataclasses import dataclass
from typing import List
from django.db import models

from apps.activitylog import constants as const
from apps.activitylog.models import TaskActivityLog
from core.services.baseservice import BaseService, GetObjectsByIdService
from apps.projects.models.tasks import Task


@dataclass
class TaskLogCreator(GetObjectsByIdService, BaseService):
    task: Task | int
    update_fields: list

    def __post_init__(self):
        self.load_objects()

    def execute(self) -> list[models.Model]:
        user = self.task.updated_by
        common_data = self._get_common_data(user)

        logs = [
            self._create_log_entry(field, common_data, user)
            for field in self.get_update_fields()
        ]
        return self.create_log(logs)

    def _get_common_data(self, user) -> dict:
        return {
            "project_id": self.task.project.id,
            "workspace_id": self.task.workspace.id,
            "task_id": self.task.id,
            "user_id": user.id,
            "timestamp": self.task.updated_at,
        }

    def _create_log_entry(self, field: str, common_data: dict, user) -> dict:
        value = getattr(self.task, field, None)
        action_type = self.get_action(field, value)
        detail = self.get_detail(action_type, field, value, user)

        return {
            **common_data,
            "field": field,
            "value": value,
            "action_type": action_type,
            "detail": detail,
        }

    def create_log(self, logs_list: List[dict]) -> list[TaskActivityLog]:
        return [TaskActivityLog.objects.create(**log) for log in logs_list]

    def get_update_fields(self) -> List[str]:
        excluded_fields = {"updated_at", "updated_by", "archive_at"}
        return [field for field in self.update_fields if field not in excluded_fields]

    def get_action(self, field: str, value: str) -> str:
        actions = {
            "module": const.ADD if value else const.REMOVE,
        }
        return actions.get(field, const.SET)

    def get_detail(self, action: str, field: str, value: str, user: str) -> str:
        base_detail = f"{user.username} {action} {field}"
        specifics = {
            const.ADD: f" added this task to module {value}",
            const.REMOVE: " removed the task from the module",
        }
        return specifics.get(action, f"{base_detail} {value}")
