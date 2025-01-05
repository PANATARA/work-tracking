from dataclasses import dataclass
from django.db import models

from apps.activitylog.models import TaskActivityLog
from apps.activitylog import constants as const
from core.services.baseservice import BaseService, GetObjectsByIdService
from apps.projects.models.tags import TaskTag
from apps.projects.models.tasks import Task
from apps.users.models.users import User


@dataclass
class M2MTaskLogCreator(GetObjectsByIdService, BaseService):
    task: Task | int
    action: str
    detailed_information: str | None

    def __post_init__(self):
        self.load_objects()

    def execute(self) -> list[models.Model]:
        user = self.task.updated_by
        action_type = self.get_action_type(self.action)
        objects_names = self.get_names_of_related_objects(self.objects_ids)
        detail = self.get_detail(
            user, 
            self.field, 
            objects_names, 
            self.action
        )
        data = {
            "project_id": self.task.project.id,
            "workspace_id": self.task.workspace.id,
            "task_id": self.task.id,
            "user_id": user.id,
            "action_type": action_type,
            "field": self.field,
            "value": objects_names,
            "detail": detail,
            "timestamp": self.task.updated_at,
        }
        return self.create_log(data)
    
    def create_log(self, data: dict) -> list[models.Model]:
        instances = [
            self.log_model.objects.create(**data)
        ]
        return list(instances)

    def get_names_of_related_objects(self, objects) -> str:
        objects_names = ", ".join(
            getattr(object, "username", getattr(object, "name", None))
            for object in objects
        )
        return objects_names

    def get_action_type(self, action) -> str:
        return const.REMOVE if action == "post_remove" else const.ADD

    def get_detail(self, user, field, objects_names, action) -> str:
        """Generating detailed information"""

        if self.detailed_information is not None:

            return self.detailed_information

        if action == "post_remove":

            return (
                f"{user.username if user else ''} removed the {field}: {objects_names}"
            )

        elif action == "post_add":

            return (
                f"{user.username if user else ''} added a new {field}: {objects_names}"
            )


@dataclass
class TaskAssigneesLogCreator(M2MTaskLogCreator):

    objects_ids: list[User | int]

    def __post_init__(self):
        self.field = "assignees"
        self.linked_model = User
        self.log_model = TaskActivityLog
        self.load_objects()


@dataclass
class TaskTagsLogCreator(M2MTaskLogCreator):

    objects_ids: list[TaskTag | int]

    def __post_init__(self):
        self.field = "tags"
        self.linked_model = TaskTag
        self.log_model = TaskActivityLog
        self.load_objects()
