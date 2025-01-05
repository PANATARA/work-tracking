from apps.workspace.models.workspace import Workspace, WorkspaceMember
from apps.users.models.users import User
from apps.workspace.constant import RoleChoices
from apps.workspace.models.workspace_config import TaskState, ProjectState

        
def all_user_in_workspace(users: list[User | int], workspace: Workspace | int) -> bool:
    """Checks whether all passed users exist in the passed workspace"""
    
    workspace_id = workspace.id if isinstance(workspace, Workspace) else workspace

    user_ids = [user.id if isinstance(user, User) else user for user in users]
    
    return all(
        WorkspaceMember.objects.filter(workspace_id=workspace_id, user_id=user_id).exists()
        for user_id in user_ids
    )


def all_user_not_in_workspace(users: list[User | int], workspace: Workspace | int) -> bool:
    """Checks whether all passed users NOT exist in the passed workspace"""
    
    workspace_id = workspace.id if isinstance(workspace, Workspace) else workspace

    user_ids = [user.id if isinstance(user, User) else user for user in users]

    return all(
        not WorkspaceMember.objects.filter(workspace_id=workspace_id, user_id=user_id).exists()
        for user_id in user_ids
    )


def role_exist(role: int) -> bool:
    return RoleChoices.OBSERVER <= role <= RoleChoices.OWNER


def projects_states_in_workspace(state: ProjectState | int, workspace: Workspace | int) -> bool:
    """Checks whether project state exist in the passed workspace"""
    
    workspace_id = workspace.id if isinstance(workspace, Workspace) else workspace
    state_id = state.id if isinstance(state, ProjectState) else state
    
    return ProjectState.objects.filter(id=state_id, workspace_id=workspace_id).exists()


def tasks_states_in_workspace(state: TaskState | int, workspace: Workspace | int) -> bool:
    """Checks whether task state exist in the passed workspace"""
    
    workspace_id = workspace.id if isinstance(workspace, Workspace) else workspace
    state_id = state.id if isinstance(state, TaskState) else state
    
    return TaskState.objects.filter(id=state_id, workspace_id=workspace_id).exists()