from dataclasses import dataclass
from typing import Any
from django.utils import timezone
from django.core.exceptions import ValidationError

from apps.projects.models.modules import Module
from apps.projects.models.projects import Project
from apps.projects.models.tasks import Task
from apps.projects.services.tag_service import TagService
from apps.projects.typing import TaskData
from apps.workspace.constant import TaskStateChoices
from apps.workspace.models.workspace import Workspace
from apps.workspace.models.workspace_config import TaskState
from apps.workspace.validators import all_user_in_workspace, tasks_states_in_workspace
from apps.users.models.users import User
from core.services.baseservice import (
    BaseService,
    BaseUpdateService,
    GetObjectsByIdService,
)


@dataclass
class TaskCreatorService(GetObjectsByIdService, BaseService):
    project: Project | int
    workspace: Workspace | int
    data: TaskData

    def __post_init__(self):
        self.assignees = self.data.pop("assignees", None)
        self.raw_tags = self.data.pop("tags", None)
        self.state = self.data.pop("state_id", None)
        self.module = self.data.pop("module", None)
        self.load_objects()

    def execute(self) -> str:
        task = self.create_task()
        if self.state:
            self.task = SetTaskState(task, self.state)()
        if self.assignees:
            self.task = SetTaskAssignees(task, self.assignees)()
        if self.raw_tags:
            self.task = SetTaskTag(task, self.raw_tags)()
        if self.module:
            self.task = SetTaskModule(task, self.module)()
        return task.get_absolute_url()

    def create_task(self) -> Task:
        return Task.objects.create(
            workspace=self.workspace,
            project=self.project,
            **self.data,
        )

    def validate(self) -> None:
        if self.project.workspace != self.workspace:
            raise ValidationError("The project does not belong to this workspace")

        return super().validate()


@dataclass
class TaskUpdaterService(GetObjectsByIdService, BaseUpdateService):
    """Returns the URL of the updated task"""
    task: int | Task
    data: TaskData

    def __post_init__(self):
        self.load_objects()
        self.assignees = self.data.pop("assignees", None)
        self.raw_tags = self.data.pop("tags", None)
        self.state = self.data.pop("state_id", None)
        self.module = self.data.pop("module", None)


    def execute(self) -> str:
        if self.state:
            self.task = SetTaskState(self.task, self.state)()
        if self.assignees:
            self.task = SetTaskAssignees(self.task, self.assignees)()
        if self.raw_tags:
            self.task = SetTaskTag(self.task, self.raw_tags)()
        if self.module:
            self.task = SetTaskModule(self.task, self.module)()

        return super().update(self.task, self.data).get_absolute_url()


@dataclass        
class SetTaskState(GetObjectsByIdService, BaseUpdateService):
    task: int | Task
    state: int | TaskState

    def __post_init__(self):
        self.load_objects()
        self.workspace = self.task.workspace

    def execute(self) -> Any:
        self.set_archive_date()
        return super().update(self.task, {"state":self.state})
    
    def set_archive_date(self) -> bool:
        """Returns True if the archiving date has changed, False otherwise"""
        past_archive_date = self.task.archive_at

        if self.state.type == TaskStateChoices.COMPLETED:
            self.task.archive_at = (
                timezone.now() + self.workspace.configuration.archive_after
            )
        else:
            self.task.archive_at = None

        return past_archive_date != self.task.archive_at
 
    def validate(self) -> None:
        workspace = self.task.workspace
        if not tasks_states_in_workspace(self.state, workspace):
            raise ValidationError("The state does not belong to this workspace")
        super().validate()


@dataclass   
class SetTaskTag(GetObjectsByIdService, BaseUpdateService):
    task: int | Task
    raw_tags: list[str]

    def __post_init__(self):
        self.load_objects()

    def execute(self) -> Any:
        tags = TagService.get_tags_entity_by_string(self.raw_tags)
        return super().update(self.task, {"tags":tags})
    

@dataclass
class SetTaskAssignees(GetObjectsByIdService, BaseUpdateService):
    task: int | Task
    assignees: list[int | User]

    def __post_init__(self):
        self.load_objects()
        self.workspace = self.task.workspace

    def execute(self) -> Any:
        return super().update(self.task, {"assignees":self.assignees})
    
    def validate(self) -> None:
        if not all_user_in_workspace(self.assignees, self.workspace):
            raise ValidationError("Not all users were found in this workspace")
        return super().validate()


@dataclass
class SetTaskModule(GetObjectsByIdService, BaseUpdateService):
    """
    Service for assigning a task to a module.

    Currently, this service performs a basic operation to set the module for a task.
    In the future, more advanced business logic might be added here.
    """
    task: int | Task
    module: int | Module

    def __post_init__(self):
        self.load_objects()

    def execute(self) -> Any:
        return super().update(self.task, {"module":self.module})
    
    def validate(self) -> None:
        if self.task.project != self.module.project:
            raise ValidationError("The module does not belong to this project")
        return super().validate()