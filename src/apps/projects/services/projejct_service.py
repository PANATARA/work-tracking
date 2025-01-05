from dataclasses import dataclass
from rest_framework.exceptions import ValidationError

from core.services.baseservice import BaseService, BaseUpdateService, GetObjectsByIdService
from apps.projects.models.projects import Project
from apps.projects.typing import ProjectData
from apps.users.models.users import User
from apps.workspace.models.workspace import Workspace
from apps.workspace.models.workspace_config import ProjectState
from apps.workspace.validators import all_user_in_workspace, projects_states_in_workspace


@dataclass
class ProjectCreatorService(BaseService, GetObjectsByIdService):
    """Return the project url after creating a project"""
    workspace: Workspace | int
    data: ProjectData

    def __post_init__(self):
        self.load_objects()
        self.manager = self.data.pop("manager", None)
        self.state = self.data.pop("state", None)

    def execute(self) -> str:
        project = self.create_project(self.data)
        project = SetProjectManager(project, self.manager if self.manager else self.workspace.owner)()
        project = SetProjectState(project, self.state)() if self.state else project

        self.send_notification(project)

        return project.get_absolute_url()

    def create_project(self, data: dict) -> Project:
        return Project.objects.create(
            workspace=self.workspace,
            **data
        )
    
    def send_notification(self, project: Project):
        #TODO: Implement this method
        pass


@dataclass
class ProjectUpdateService(GetObjectsByIdService, BaseUpdateService):
    """Returns the URL of the updated project"""
    project: int | Project
    data: ProjectData | None

    def __post_init__(self):
        self.load_objects()
        self.manager = self.data.pop("manager", None)
        self.state = self.data.pop("state", None)

    def execute(self) -> str:
        self.project = SetProjectManager(self.project, self.manager)() if self.manager else self.project
        self.project = SetProjectState(self.project, self.state)() if self.state else self.project

        return self.project.get_absolute_url()

@dataclass
class SetProjectState(GetObjectsByIdService, BaseUpdateService):
    """
    Service to set the state of a project.

    Return: Project object
    """
    project: Project | int
    state: ProjectState | int

    def __post_init__(self):
        self.load_objects()

    def execute(self):
        return super().update(self.project, {"state": self.state})
    
    def validate(self):
        if not projects_states_in_workspace(self.state, self.project.workspace.id):
            raise ValidationError("This workspace does not have this project state")
        return super().validate()

@dataclass
class SetProjectManager(GetObjectsByIdService, BaseUpdateService):
    """
    Service to set the manager of a project.

    Return: Project object
    """
    project: Project | int
    manager: User | int

    def __post_init__(self):
        self.load_objects()

    def execute(self):
        return super().update(self.project, {"manager": self.manager})
    
    def validate(self):
        if not all_user_in_workspace([self.manager], self.project.workspace.id):
            raise ValidationError("This user does not exist in the workspace")
        return super().validate()
