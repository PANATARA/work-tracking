from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.workspace.schema import member_schema, workspace_logout_schema
from core.views.mixins import BasePermissionByActionView
from apps.workspace.constant import RoleChoices
from apps.workspace.models.workspace import Workspace, WorkspaceMember
from apps.workspace.permissions import IsWorkspaceAdmin, IsWorkspaceMember
from apps.workspace.serializers.api.workspace_members import MemberSerializer
from apps.workspace.services.workspace_member import MemberKickService, MemberLogoutService, WorkspaceMemberService



@member_schema
class WorkspaceMembersView(BasePermissionByActionView, ModelViewSet):
    permission_classes_by_action = {
        "list": [IsWorkspaceMember],
        "retrieve": [IsWorkspaceMember],
        "partial_update": [IsWorkspaceAdmin],
        "destroy": [IsWorkspaceAdmin],
    }
    serializer_class = MemberSerializer

    http_method_names = ("get", "patch", "delete")

    lookup_url_kwarg = "user_id"
    lookup_field = "user"

    def get_queryset(self):
        workspace_id = self.kwargs.get("workspace_id")
        return WorkspaceMember.objects.filter(
            workspace_id=workspace_id
        ).select_related(
            "user__user_avatar",
        )
    
    def destroy(self, request, *args, **kwargs):
        workspace_id = self.kwargs.get("workspace_id")
        kicked_user = self.kwargs.get("user_id")

        MemberKickService(kicked_user, workspace_id)()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        workspace_id = self.kwargs.get("workspace_id")
        workspace = Workspace.objects.get(pk=workspace_id)

        WorkspaceMemberService.member_update_role(
            workspace=workspace,
            user=instance.user,
            new_role=serializer.validated_data.get("role", RoleChoices.MEMBER)
        )

        return Response()


@workspace_logout_schema
class WorkspaceMembersLogoutAPI(GenericAPIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["delete"]

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        workspace_id = kwargs.get("workspace_id")

        MemberLogoutService(user, workspace_id)()
        return Response(status=status.HTTP_204_NO_CONTENT)
