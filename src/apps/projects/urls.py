from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.projects.views import modules, projects, tasks

router = DefaultRouter()

router.register(
    r"workspace/(?P<workspace_id>\d+)/projects",
    projects.ProjectView,
    "projects",
)
router.register(
    r"workspace/(?P<workspace_id>\d+)/projects/(?P<project_id>\d+)/modules",
    modules.ModuleView,
    "project-modules",
)
router.register(
    r"workspaces/(?P<workspace_id>\d+)/projects/(?P<project_id>\d+)/tasks",
    tasks.TaskViewSet,
    basename="project-task",
)
router.register(
    r"workspaces/(?P<workspace_id>\d+)/projects/(?P<project_id>\d+)/tasks",
    tasks.ArchivedTasksViewSet,
    basename="project-archived-task",
)

router.register(r"dashboard/tasks", tasks.DashboardTaskView, "dashboard-tasks")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "workspace/<int:workspace_id>/transfer/tasks/",
        tasks.TransferTaskBetweenModuleView.as_view(),
        name="transfer-tasks",
    ),
    path(
        "workspace/<int:workspace_id>/restore/tasks/<int:task_id>",
        tasks.RestoreArchivedTaskView.as_view(),
        name="restore-tasks",
    ),
    path(
        "workspace/<int:workspace_id>/archive/tasks/<int:task_id>",
        tasks.ArchiveTaskView.as_view(),
        name="archive-tasks",
    ),
    path(
        "workspace/<int:workspace_id>/subscribe/tasks/<int:task_id>",
        tasks.SubscribeUserToTaskView.as_view(),
        name="subscribe-tasks",
    ),
    path(
        "workspace/<int:workspace_id>/unsubscribe/tasks/<int:task_id>",
        tasks.UnsubscribeUserToTaskView.as_view(),
        name="unsubscribe-tasks",
    ),
]
