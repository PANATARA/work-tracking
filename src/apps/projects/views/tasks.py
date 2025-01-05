from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    get_object_or_404 as get_object_or_HTTP404,
)
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import (
    Case,
    When,
    BooleanField,
    Exists,
    OuterRef,
    Prefetch,
    Subquery,
)

from apps.projects import filters
from apps.projects.serializers import tasks as srlzr
from apps.projects.models.tasks import Task, TaskSubscriber
from apps.projects.services.task_service import TaskCreatorService, TaskUpdaterService
from apps.projects.services.tasks_subscribe import (
    SubscribeUserToTaskService,
    UnsubscribeUserToTaskService,
)
from apps.projects.services.task_transfer import TransferTasksService
from apps.projects.schema import (
    dashboard_task,
    transfer_task_between_module_schema,
    restore_archived_task,
    archived_task_schema,
    archive_task,
    subscribe_user_to_task_schema,
    unsubscribe_user_to_task_schema,
    task_schema,
)
from apps.projects.typing import TaskData
from apps.users.models.users import User
from apps.workspace.constant import RoleChoices
from apps.workspace.models.workspace import WorkspaceMember
from apps.workspace.permissions import workspace_permission_by_role


@task_schema
class TaskViewSet(GenericViewSet):
    http_method_names = ["get", "patch", "post", "delete"]
    lookup_url_kwarg = "task_id"

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return srlzr.TaskReadOnlySerializer
        elif self.action == "partial_update":
            return srlzr.TaskUpdateSerializer
        elif self.action == "create":
            return srlzr.TaskCreateSerializer

    def get_task_manager(self):
        return Task.objects

    def get_queryset(self):
        workspace_id = self.kwargs.get("workspace_id")
        project_id = self.kwargs.get("project_id")
        user = self.request.user

        role_subquery = WorkspaceMember.objects.filter(
            workspace_id=workspace_id, user_id=OuterRef("pk")
        ).values("role")[:1]

        return (
            self.get_task_manager()
            .filter(project=project_id)
            .select_related(
                "module__project",
                "module__workspace",
                "project__workspace",
                "project__state",
                "workspace__owner__user_avatar",
                "state",
            )
            .prefetch_related(
                "tags",
                Prefetch(
                    "assignees",
                    queryset=User.objects.select_related("user_avatar").annotate(
                        role=Subquery(role_subquery)
                    ),
                ),
            )
            .annotate(
                is_subscriber=Case(
                    When(
                        Exists(
                            TaskSubscriber.objects.filter(
                                task=OuterRef("pk"), subscriber=user
                            )
                        ),
                        then=True,
                    ),
                    default=False,
                    output_field=BooleanField(),
                )
            )
        )

    @workspace_permission_by_role(RoleChoices.MEMBER)
    def list(self, request, workspace_id, project_id):
        tasks = self.get_queryset()
        serializer = srlzr.TaskReadOnlySerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @workspace_permission_by_role(RoleChoices.MANAGER)
    def retrieve(self, request, workspace_id, project_id, task_id=None):
        task = self.get_object()
        serializer = srlzr.TaskReadOnlySerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @workspace_permission_by_role(RoleChoices.MANAGER)
    def partial_update(self, request, workspace_id, project_id, task_id):
        serializer = srlzr.TaskUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        task_absolute_url = TaskUpdaterService(
            task=task_id, 
            data=TaskData(**validated_data)
        )()

        return Response(
            data={"absolute_url": task_absolute_url}, status=status.HTTP_200_OK
        )

    @workspace_permission_by_role(RoleChoices.MANAGER)
    def create(self, request, workspace_id, project_id):
        serializer = srlzr.TaskCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        task_absolute_url = TaskCreatorService(
            project=project_id,
            workspace=workspace_id,
            data=TaskData(**validated_data),
        )()

        return Response(
            data={"absolute_url": task_absolute_url}, status=status.HTTP_201_CREATED
        )

    @workspace_permission_by_role(RoleChoices.MANAGER)
    def destroy(self, request, workspace_id, project_id, task_id):
        task = get_object_or_HTTP404(Task, pk=task_id)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@archived_task_schema
class ArchivedTasksViewSet(TaskViewSet):

    http_method_names = ("get", "delete")

    def get_task_manager(self):
        return Task.archive_objects


@restore_archived_task
class RestoreArchivedTaskView(APIView):
    queryset = Task.archive_objects.all()

    http_method_names = ["patch"]
    lookup_url_kwarg = "task_id"

    @workspace_permission_by_role(RoleChoices.MANAGER)
    def patch(self, request, workspace_id, task_id):
        instance = get_object_or_HTTP404(self.queryset, pk=task_id)
        data = {
            "is_archive": False,
            "archive_at": None,
            "state": None,
        }
        TaskUpdaterService(instance, data)()
        return Response(status=status.HTTP_204_NO_CONTENT)


@archive_task
class ArchiveTaskView(APIView):
    queryset = Task.objects.all()

    http_method_names = ["patch"]
    lookup_url_kwarg = "task_id"

    @workspace_permission_by_role(RoleChoices.MANAGER)
    def patch(self, request, workspace_id, task_id):
        instance = get_object_or_HTTP404(self.queryset, pk=task_id)
        data = {
            "is_archive": True,
            "archive_at": timezone.now(),
            "state": None,
        }
        TaskUpdaterService(instance, data)()
        return Response(status=status.HTTP_204_NO_CONTENT)


@dashboard_task
class DashboardTaskView(GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = srlzr.DashboardTaskSerializer

    http_method_names = [
        "get",
    ]

    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    )
    filterset_class = filters.DashboardTaskFilter
    search_fields = [
        "title",
        "description",
    ]
    ordering = ("created_at", "priority")

    def get_queryset(self):
        user = self.request.user
        return (
            Task.objects.filter(assignees=user)
            .select_related(
                "project",
                "module",
            )
            .prefetch_related("assignees", "tags")
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


@transfer_task_between_module_schema
class TransferTaskBetweenModuleView(CreateAPIView):
    serializer_class = srlzr.TaskTransferSerializer

    @workspace_permission_by_role(RoleChoices.ADMIN)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = TransferTasksService(
            tasks_ids=serializer.validated_data["task"],
            module_id=serializer.validated_data["module"],
        )()

        headers = self.get_success_headers(serializer.data)
        return Response(data=message, status=status.HTTP_200_OK, headers=headers)


@subscribe_user_to_task_schema
class SubscribeUserToTaskView(CreateAPIView):
    http_method_names = ["post"]

    @workspace_permission_by_role(RoleChoices.MEMBER)
    def create(self, request, *args, **kwargs):
        user = request.user
        task = kwargs.get("task_id")
        if not TaskSubscriber.objects.filter(subscriber=user, task=task).exists():
            subscribe = [TaskSubscriber(task_id=task, subscriber=user)]
            SubscribeUserToTaskService.create_task_subscriber(subscribe)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                data="User already subscribed to this task",
                status=status.HTTP_400_BAD_REQUEST,
            )


@unsubscribe_user_to_task_schema
class UnsubscribeUserToTaskView(DestroyAPIView):
    http_method_names = ["delete"]

    @workspace_permission_by_role(RoleChoices.MEMBER)
    def delete(self, request, *args, **kwargs):
        user = request.user
        task = kwargs.get("task_id")

        UnsubscribeUserToTaskService.delete_task_subscription([user.id], task)

        return Response(status=status.HTTP_204_NO_CONTENT)
