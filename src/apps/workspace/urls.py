from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.workspace.views.workspace_members import (
    WorkspaceMembersLogoutAPI,
    WorkspaceMembersView,
)
from apps.workspace.views.workspace_user_config import (
    UserFavoriteView,
    UserWorkspaceConfigView,
)
from apps.workspace.views.workspace_config import (
    ResetProjectsStates,
    ResetTasksStates,
    WorkspaceConfigProjectView,
    WorkspaceConfigTaskView,
    WorkspaceConfigurationView,
)
from apps.workspace.views.workspace import ReassignWorkspaceOwnerView, WorkspaceView

router = DefaultRouter()

router.register(r"workspace", WorkspaceView, basename="workspace")
router.register(
    r"workspace/(?P<workspace_id>\d+)/members",
    WorkspaceMembersView,
    basename="workspace-members",
)
router.register(
    r"workspace/user-config", 
    UserWorkspaceConfigView, 
    basename="workspace-user-config",
)
router.register(
    r"workspace/(?P<workspace_id>\d+)/config/project/states",
    WorkspaceConfigProjectView,
    basename="workspace-project-states",
)
router.register(
    r"workspace/(?P<workspace_id>\d+)/config/task/states",
    WorkspaceConfigTaskView,
    basename="workspace-task-states",
)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "workspace/<int:workspace_id>/members/logout",
        WorkspaceMembersLogoutAPI.as_view(),
        name="workspace-members-logout",
    ),
    path(
        "workspace/<int:workspace_id>/user-favorite/",
        UserFavoriteView.as_view(),
        name="workspace-user-favorite",
    ),
    path(
        "workspace/<int:workspace_id>/reassign-owner/<int:user_id>",
        ReassignWorkspaceOwnerView.as_view(),
        name="workspace-owner-reassign",
    ),
    path(
        "workspace/<int:workspace_id>/config/projects/states/reset",
        ResetProjectsStates.as_view(),
        name="workspace-project-states-reset",
    ),
    path(
        "workspace/<int:workspace_id>/config/tasks/states/reset",
        ResetTasksStates.as_view(),
        name="workspace-tasks-states-reset",
    ),
    path(
        "workspace/<int:workspace_id>/configuration",
        WorkspaceConfigurationView.as_view(),
        name="workspace-configuration",
    ),
]
