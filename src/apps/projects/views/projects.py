from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Case, When, Count, Q

from apps.projects.filters import ProjectFilter
from apps.projects.models.projects import Project
from apps.projects.serializers import projects
from apps.projects.schema import project_schema
from apps.projects.services.projejct_service import ProjectCreatorService, ProjectUpdateService
from apps.projects.typing import ProjectData
from apps.workspace.constant import RoleChoices
from apps.workspace.permissions import workspace_permission_by_role

@project_schema
class ProjectView(GenericViewSet):
    http_method_names = ("get", "post", "patch", "delete")
    lookup_url_kwarg = "project_id"

    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    )
    filterset_class = ProjectFilter
    search_fields = [
        "name",
        "description",
    ]
    ordering = "-created_at"

    def get_queryset(self):
        user = self.request.user
        workspace_id = self.kwargs["workspace_id"]

        return (
            Project.objects.filter(
                workspace_id=workspace_id,
            )
            .select_related(
                "workspace__owner__user_avatar",
                "manager__user_avatar",
                "state",
            )
            .annotate(
                user_is_author=Case(
                    When(created_by=user, then=True),
                    default=False,
                ),
                user_is_manager=Case(
                    When(manager=user, then=True),
                    default=False,
                ),
                total_active_tasks=Count(
                    "tasks", distinct=True, filter=Q(tasks__is_archive=False)
                ),
                total_archived_tasks=Count(
                    "tasks", distinct=True, filter=Q(tasks__is_archive=True)
                ),
            )
        )

    def get_serializer_class(self):
        if self.action in ["update", "partial_update", "create"]:
            return projects.ProjectCreateUpdateSerializer
        if self.action in ["retrieve", "list"]:
            return projects.ProjectReadOnlySerializer

    @workspace_permission_by_role(RoleChoices.MEMBER)
    def list(self, request, *args, **kwargs):
        projects_queryset = self.get_queryset()
        if not projects:
            return Response({"detail": "Projects not found"}, status=status.HTTP_200_OK)
        serializer = self.get_serializer(projects_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @workspace_permission_by_role(RoleChoices.MEMBER)
    def retrieve(self, request, *args, **kwargs):
        project = self.get_object()
        serializer = self.get_serializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @workspace_permission_by_role(RoleChoices.ADMIN)
    def partial_update(self, request, *args, **kwargs):
        serializer = projects.ProjectCreateUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        project_id = self.kwargs.get("project_id")
        validated_data = serializer.validated_data

        project_absolute_url = ProjectUpdateService(
            project=project_id,
            data=ProjectData(**validated_data),
        )()

        return Response(
            data={"absolute_url":project_absolute_url},  
            status=status.HTTP_200_OK
        )

    @workspace_permission_by_role(RoleChoices.ADMIN)
    def create(self, request, *args, **kwargs):
        serializer = projects.ProjectCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        workspace_id = self.kwargs.get("workspace_id")
        validated_data = serializer.validated_data

        project_absolute_url = ProjectCreatorService(
            workspace=workspace_id,
            data=ProjectData(**validated_data),
        )()

        return Response(
            data={"absolute_url":project_absolute_url}, 
            status=status.HTTP_201_CREATED
        )

    @workspace_permission_by_role(RoleChoices.ADMIN)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
