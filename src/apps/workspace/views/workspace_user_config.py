from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Prefetch

from apps.projects.models.modules import Module
from apps.users.models.users import User
from apps.workspace.constant import RoleChoices
from apps.workspace.models.workspace_config import TaskState
from apps.workspace.schema import user_workspace_config, user_workspace_favorite
from apps.workspace.models.workspace_user_config import UserWorkspaceConfig, UserFavorite
from apps.workspace.permissions import IsUsersConfig, IsWorkspaceMember, workspace_permission_by_role
from apps.workspace.serializers.api.workspace_user_config import (
    UserFavoriteCreateSerializer,
    UserFavoriteReadSerializer,
    UserFavoriteUpdateSerializer,
    UserWorkspaceConfigSerializer,
)
from apps.workspace.services.workspace_user_config import UserFavoriteCreator


@user_workspace_config
class UserWorkspaceConfigView(GenericViewSet):

    permission_classes = [IsUsersConfig]
    serializer_class = UserWorkspaceConfigSerializer

    http_method_names = ("get", "patch", "put")

    lookup_field = "workspace_id"

    def get_queryset(self):
        user = self.request.user
        queryset = UserWorkspaceConfig.objects.filter(
            user=user,
        ).select_related(
            "user__user_avatar",
            "workspace__owner__user_avatar",
            "filters",
            "properties",
        ).prefetch_related(
            Prefetch(
                "filters__state",
                queryset=TaskState.objects.only("id", "name", "type"),
            ),
            Prefetch(
                "filters__assignee",
                queryset=User.objects.select_related("user_avatar").only("id", "username", "user_avatar"),
            ),
            Prefetch(
                "filters__module",
                queryset=Module._base_manager.only("id", "name", "status"),
            ),
            Prefetch(
                "filters__created_by",
                queryset=User.objects.select_related("user_avatar").only("id", "username", "user_avatar"),
            ),
        )
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UserWorkspaceConfigSerializer(
            instance, data=request.data, partial=True
        )

        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)


@user_workspace_favorite
class UserFavoriteView(APIView):

    http_method_names = ("get", "patch", "post", "delete")
    # permission_classes = [IsWorkspaceMember]

    def get_queryset(self):
        user = self.request.user
        workspace_id=self.kwargs.get("workspace_id")
        queryset = UserFavorite.objects.filter(
            user=user,
            workspace_id=workspace_id,
        ).select_related(
            "user__user_avatar",
            "workspace__owner__user_avatar",
        ).order_by("sequence")
        return queryset

    @workspace_permission_by_role(RoleChoices.MEMBER)
    def get(self, request, workspace_id):
        queryset = self.get_queryset()

        serializer = UserFavoriteReadSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @workspace_permission_by_role(RoleChoices.MEMBER)
    def post(self, request, workspace_id):
        serializer = UserFavoriteCreateSerializer(data=request.data)

        if serializer.is_valid():
            favorite = UserFavoriteCreator(
                user=request.user,
                workspace=workspace_id,
                data=serializer.validated_data,
            )()
            read_serializer = UserFavoriteReadSerializer(favorite)
            return Response(read_serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @workspace_permission_by_role(RoleChoices.MEMBER)
    def patch(self, request, workspace_id, favorite_id):

        instance = UserFavorite.objects.get(
            user=request.user, workspace_id=workspace_id, pk=favorite_id
        )
        serializer = UserFavoriteUpdateSerializer(
            instance, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @workspace_permission_by_role(RoleChoices.MEMBER)
    def delete(self, request, workspace_id, favorite_id):
        favorite = UserFavorite.objects.get(
            user=request.user, workspace_id=workspace_id, pk=favorite_id
        )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
