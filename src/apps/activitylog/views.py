from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from apps.activitylog import serializers
from apps.activitylog.models import TaskActivityLog
from apps.workspace.permissions import IsWorkspaceMember
from apps.activitylog.schema import (
    task_log_activity,
    user_tasks_logs_activities,
    user_recent_tasks_logs_activities,
)


@task_log_activity
class ListTaskLogsView(GenericViewSet):
    """Gets all task logs"""

    permission_classes = [IsWorkspaceMember]
    serializer_class = serializers.ListTaskLogsSerializer

    http_method_names = ("get",)
    lookup_url_kwarg = "task_id"

    def get_queryset(self):
        task_id = self.kwargs.get("task_id")
        return TaskActivityLog.objects.filter(
            task=task_id,
        ).select_related(
            "user",
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not queryset.exists():
            return Response(
                {"detail": "Task logs not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@user_tasks_logs_activities
class UserAllTaskActvity(APIView):
    """Gets the all task logs triggered by the current user in the specified workspace."""

    permission_classes = [IsAuthenticated]
    http_method_names = ("get",)

    def get_queryset(self, workspace_id):
        user = self.request.user
        return TaskActivityLog.objects.filter(
            user=user, workspace=workspace_id
        ).select_related(
            "task",
            "user__user_avatar",
        )

    def get(self, request, workspace_id):
        queryset = self.get_queryset(workspace_id)

        if not queryset.exists():
            return Response(
                {"detail": "Task logs not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = serializers.ListTaskLogsSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@user_recent_tasks_logs_activities
class UserRecentTaskActvity(UserAllTaskActvity):
    """Gets the most recent 10 task logs triggered by the current user in the specified workspace."""

    def get_queryset(self, workspace_id):
        return super().get_queryset(workspace_id)[:10]
