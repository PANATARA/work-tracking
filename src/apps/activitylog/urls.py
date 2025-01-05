from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views 

router = DefaultRouter()

router.register(r'workspace/(?P<workspace_id>\d+)/logs/activities/tasks/(?P<task_id>\d+)', views.ListTaskLogsView, 'tasks-activities')

urlpatterns = [
    path('', include(router.urls)),
    path(
        "workspace/<int:workspace_id>/activities/tasks/recent/logs/user/",
        views.UserRecentTaskActvity.as_view(),
        name="tasks-recent-logs-user",
    ),
    path(
        "workspace/<int:workspace_id>/activities/tasks/logs/user",
        views.UserAllTaskActvity.as_view(),
        name="tasks-all-logs-user",
    ),

]