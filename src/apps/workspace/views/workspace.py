from rest_framework.viewsets import ModelViewSet
from django.db.models import Count, Q, Prefetch
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from apps.workspace.constant import RoleChoices
from apps.workspace.schema import reassign_workspace_owner_schema, workspace
from core.views.mixins import BasePermissionByActionView
from apps.workspace.models.workspace import Workspace, WorkspaceMember
from apps.workspace.serializers.api import workspace as wp
from apps.workspace.permissions import IsWorkspaceMember, IsWorkspaceAdmin, IsWorkspaceOwner, workspace_permission_by_role
from apps.workspace.services.workspace_creator import (
    ReassignWorkspaceOwner,
    WorkspaceCreator,
)


@workspace
class WorkspaceView(BasePermissionByActionView, ModelViewSet):
    permission_classes_by_action = {
        "list": [IsAuthenticated],
        "create": [IsAuthenticated],
        "retrieve": [IsWorkspaceMember],
        "update": [IsWorkspaceAdmin],
        "partial_update": [IsWorkspaceAdmin],
        "destroy": [IsWorkspaceOwner],
    }
    serializer_class = wp.WorkspaceSerializer
    http_method_names = ("get", "post", "patch", "put", "delete")
    lookup_url_kwarg = "workspace_id"

    def get_queryset(self):
        user = self.request.user
        return Workspace.objects.annotate(
            total_members=Count("members", distinct=True),
            total_active_tasks=Count(
                "tasks", distinct=True, filter=Q(tasks__is_archive=False)
            ),
            total_archived_tasks=Count(
                "tasks", distinct=True, filter=Q(tasks__is_archive=True)
            ),
            ).filter(
                members=user
            ).select_related(
                "owner__user_avatar",
            ).prefetch_related(
                Prefetch(
                    "memberships",
                    queryset=WorkspaceMember.objects.select_related("user__user_avatar"),
                    to_attr="workspace_members",
                )
            )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        user = request.user
        workspace = WorkspaceCreator(
            owner=user,
            name=validated_data.get("name"),
            description=validated_data.get("description"),
        )()
        absolute_url = workspace.get_absolute_url()
        
        return Response(
            data={"absolute_url":absolute_url}, 
            status=status.HTTP_201_CREATED
        )


@reassign_workspace_owner_schema
class ReassignWorkspaceOwnerView(APIView):

    http_method_names = ["post"]

    @workspace_permission_by_role(RoleChoices.OWNER)
    def post(self, request, workspace_id, user_id):

        if user_id == request.user.id:
            return Response("You are already the owner", status=status.HTTP_200_OK)

        ReassignWorkspaceOwner(
            workspace=workspace_id,
            user=user_id,  # The user who will become the new owner
        )()

        return Response(status=status.HTTP_204_NO_CONTENT)
