from dataclasses import dataclass
from typing import Any, Callable
from django.db.models import Case, When, Value, QuerySet
from rest_framework.exceptions import ValidationError

from core.services.baseservice import BaseService, GetObjectsByIdService
from apps.projects.models.projects import Project
from apps.projects.models.tasks import Task
from apps.workspace.constant import TaskStateChoices
from apps.workspace.models.workspace import Workspace
from apps.workspace.models.workspace_config import (
    TaskState,
    ProjectState,
)
from apps.workspace.services.workspace_creator import WorkspaceCreator


@dataclass
class ResetProjectsStatesService(BaseService, GetObjectsByIdService):
    """Service for reseting projects states to default"""

    workspace: Workspace | int

    def __post_init__(self):
        self.load_objects()

    def execute(self) -> None:
        current_states = list(self.get_current_states())  # because lazy query
        new_states = self.create_default_states()
        self.update_and_cleanup_states(current_states, new_states)
        return

    def update_and_cleanup_states(
        self,
        old_states: list[ProjectState],
        new_states: dict[ProjectState.type : ProjectState],
    ) -> None:
        """Replaces old states with new ones and deletes the old states"""

        Project.objects.filter(workspace=self.workspace).update(
            state_id=Case(
                *[
                    When(
                        state_id=old_state.id,
                        then=Value(new_states[old_state.type].id),
                    )
                    for old_state in old_states
                ],
                default=Value(None)
            )
        )
        for state in old_states:
            state.delete()

    def create_default_states(self) -> dict[ProjectState.type : ProjectState]:
        return {
            state.type: state
            for state in WorkspaceCreator.create_projects_states(self.workspace, None)
        }

    def get_current_states(self) -> QuerySet:
        return ProjectState.objects.filter(workspace=self.workspace)


@dataclass
class ResetTasksStatesService(BaseService, GetObjectsByIdService):
    """Service for reseting tasks states to default"""

    workspace: Workspace | int

    def __post_init__(self):
        self.load_objects()

    def execute(self) -> None:
        current_states = list(self.get_current_states())  # because lazy query
        new_states = self.create_default_states()
        self.update_and_cleanup_states(current_states, new_states)
        return

    def update_and_cleanup_states(
        self,
        old_states: list[TaskState],
        new_states: dict[TaskState.type : TaskState],
    ) -> None:
        """Replaces old states with new ones and deletes the old states"""

        Task.objects.filter(workspace=self.workspace).update(
            state_id=Case(
                *[
                    When(
                        state_id=old_state.id,
                        then=Value(new_states[old_state.type].id),
                    )
                    for old_state in old_states
                ],
                default=Value(None)
            )
        )
        for state in old_states:
            state.delete()

    def create_default_states(self) -> dict[TaskState.type : TaskState]:
        return {
            state.type: state
            for state in WorkspaceCreator.create_tasks_states(self.workspace, None)
        }

    def get_current_states(self) -> QuerySet:
        return TaskState.objects.filter(workspace=self.workspace)
