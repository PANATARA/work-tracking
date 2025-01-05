from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework import status

from core.views.mixins import BasePermissionByActionView, BasePermissionByHTTPMethod
from apps.workspace.permissions import IsWorkspaceAdmin, IsWorkspaceMember
from apps.workspace.models.workspace_config import (
    TaskState,
    ProjectState,
    WorkspaceConfiguration,
)
from apps.workspace.serializers.workspace_config import (
    TaskStatesSerializer,
    ProjectStatesSerializer,
    WorkspaceConfigurationSerializer,
)
from apps.workspace.schema import (
    workspace_project_config,
    workspace_project_config_reset_states,
    workspace_task_config,
    workspace_task_config_reset_states,
    workspace_config,
)
from apps.workspace.services.reset_states import ResetProjectsStatesService, ResetTasksStatesService


@workspace_config
class WorkspaceConfigurationView(BasePermissionByHTTPMethod, RetrieveUpdateAPIView):
    permission_classes_by_method = {
        "GET": [IsWorkspaceMember],
        "PATCH": [IsWorkspaceAdmin],
    }
    serializer_class = WorkspaceConfigurationSerializer

    http_method_names = ("get", "patch")
    lookup_field = "workspace_id"

    def get_queryset(self):
        workspace_id = self.kwargs.get("workspace_id")
        return WorkspaceConfiguration.objects.filter(workspace_id=workspace_id)


@workspace_project_config
class WorkspaceConfigProjectView(BasePermissionByActionView, ModelViewSet):
    permission_classes_by_action = {
        "list": [IsWorkspaceMember],
        "create": [IsWorkspaceAdmin],
        "retrieve": [IsWorkspaceMember],
        "destroy": [IsWorkspaceAdmin],
    }
    serializer_class = ProjectStatesSerializer

    http_method_names = ("get", "post", "delete")
    lookup_url_kwarg = "state_id"

    def get_queryset(self):
        workspace_id = self.kwargs.get("workspace_id")
        return ProjectState.objects.filter(workspace=workspace_id)


@workspace_task_config
class WorkspaceConfigTaskView(BasePermissionByActionView, ModelViewSet):
    permission_classes_by_action = {
        "list": [IsWorkspaceMember],
        "create": [IsWorkspaceAdmin],
        "retrieve": [IsWorkspaceMember],
        "destroy": [IsWorkspaceAdmin],
    }
    serializer_class = TaskStatesSerializer

    http_method_names = ("get", "post", "delete")
    lookup_url_kwarg = "state_id"

    def get_queryset(self):
        workspace_id = self.kwargs.get("workspace_id")
        return TaskState.objects.filter(workspace=workspace_id)

@workspace_project_config_reset_states
class ResetProjectsStates(APIView):
    http_method_names = ["post"]
    permission_classes = [IsWorkspaceAdmin]

    def post(self, request, workspace_id):
        ResetProjectsStatesService(workspace=workspace_id)()
        return Response(status=status.HTTP_200_OK)

@workspace_task_config_reset_states
class ResetTasksStates(APIView):
    http_method_names = ["post"]
    permission_classes = [IsWorkspaceAdmin]

    def post(self, request, workspace_id):
        ResetTasksStatesService(workspace=workspace_id)()
        return Response(status=status.HTTP_200_OK)