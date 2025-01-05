from dataclasses import dataclass
from django.utils.text import slugify
from typing import Any, Callable, Optional
from django.db import transaction
from rest_framework.exceptions import ValidationError

from core.services.baseservice import BaseService, GetObjectsByIdService
from apps.workspace.constant import RoleChoices, TaskStateChoices, ProjectStateChoices
from apps.workspace.models.workspace import Workspace
from apps.users.models.users import User
from apps.workspace.models.workspace_config import TaskState, ProjectState, WorkspaceConfiguration
from apps.workspace.services.workspace_member import WorkspaceMemberService
from apps.workspace.validators import all_user_in_workspace

@dataclass
class WorkspaceCreator(BaseService, GetObjectsByIdService):
    """
    Service for creating a workspace

    Functionality:
    - Create a Workspace: Initializes a new workspace with the provided name.
    - Assign Ownership: Adds the user as a participant in the workspace with the role of "Owner."
    - Set Up Project States: Generates default project states for the workspace.
    - Set Up Task States: Creates default task states for task management within the workspace.
    - Initialize Configuration: Establishes default settings for the workspace using a configuration model.
    """
    owner: User | int
    name: str
    description: Optional[str] = None

    def __post_init__(self):
        self.load_objects()

    def execute(self) -> Workspace:
        fields = {
            'name': self.name,
            'description': self.description,
            'slug': self.generate_slug(self.name),
            'owner': self.owner,
        }
        with transaction.atomic():
            workspace = self.create_workspace(fields)
            self.setup_workspace_dependencies(workspace)
        return workspace

    def generate_slug(self, string: str) -> str:
        return slugify(string)

    def create_workspace(self, fields: dict[str, any]) -> Workspace:
        return Workspace.objects.create(**fields)

    def setup_workspace_dependencies(self, workspace: Workspace) -> None:
        
        # Create a first member with role Owner
        users_with_roles = [{"user": self.owner, "role": RoleChoices.OWNER}]
        WorkspaceMemberService(workspace, users_with_roles)()

        # Workspace dependencies
        self.create_projects_states(workspace, ProjectStateChoices.DEFAULT_STATE)
        self.create_tasks_states(workspace, TaskStateChoices.DEFAULT_STATE)
        WorkspaceConfiguration.objects.create(workspace = workspace)

    @staticmethod
    def create_projects_states(workspace: Workspace, states: dict[str, int] | None) -> list[ProjectState]:
        if states is None:
            states = ProjectStateChoices.DEFAULT_STATE
        result_list = list()
        for name, state_type in states.items():
            result_list.append(
                ProjectState.objects.create(
                    workspace=workspace,
                    name=name,
                    type=state_type,
                )
            )
        return result_list

    @staticmethod
    def create_tasks_states(workspace: Workspace, states: dict[str, int] | None) -> list[TaskState]:
        if states is None:
            states = TaskStateChoices.DEFAULT_STATE
        result_list = list()
        for name, state_type in states.items():
            result_list.append(
                TaskState.objects.create(
                    workspace=workspace,
                    name=name,
                    type=state_type,
                )
            )
        return result_list


@dataclass
class ReassignWorkspaceOwner(BaseService, GetObjectsByIdService):
    """Service for reassigning the owner of a workspace"""
    workspace: Workspace | int
    user: User | int

    def __post_init__(self):
        self.load_objects()

    def execute(self) -> None:
        former_owner = self.workspace.owner

        self.workspace.owner = self.user
        self.workspace.save()

        users_with_roles = [
            {"user": self.user, "role": RoleChoices.OWNER},
            {"user": former_owner, "role": RoleChoices.ADMIN}
        ]
        WorkspaceMemberService(self.workspace, users_with_roles)()
    
    def get_validators(self) -> list[Callable[..., Any]]:
        return [
            self.validate_user
        ]
    
    def validate_user(self):
        if not all_user_in_workspace([self.user], self.workspace):
            raise ValidationError(f"The user {self.user.username}  is not in this workspace ")
            