from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import UpdateModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Case, When, IntegerField

from apps.projects.models.modules import Module
from apps.projects.serializers import modules
from apps.projects.schema import module_schema
from apps.workspace.permissions import workspace_permission_by_role
from apps.workspace.constant import RoleChoices, TaskStateChoices


@module_schema
class ModuleView(GenericViewSet, UpdateModelMixin, CreateModelMixin, DestroyModelMixin):
    http_method_names = ("get", "post", "patch", "delete")
    lookup_url_kwarg = "module_id"

    def get_queryset(self):
        project_id = self.kwargs.get("project_id")
        return Module.objects.filter(
                project_id=project_id
            ).select_related(
                "project__state",
                "project__workspace",
                "workspace__owner__user_avatar",
            ).annotate(
                tasks_count=Count("tasks"),
                completed_tasks_count=Count(
                    Case(
                        When(tasks__state__type=TaskStateChoices.COMPLETED, then=1),
                        output_field=IntegerField(),
                    )
                ),
            )

    def get_serializer(self, *args, **kwargs):
        kwargs["context"] = {
            "workspace_id": self.kwargs.get("workspace_id"),
            "project_id": self.kwargs.get("project_id")
        }
        return super().get_serializer(*args, **kwargs)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return modules.ModuleReadOnlySerializer
        if self.action in ["update", "partial_update", "create"]:
            return modules.ModuleUpdateCreateSerializer
    
    @workspace_permission_by_role(RoleChoices.MEMBER)
    def list(self, request, *args, **kwargs):
        modules_queryset = self.get_queryset()
        serializer = self.get_serializer(modules_queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @workspace_permission_by_role(RoleChoices.MEMBER)
    def retrieve(self, request, *args, **kwargs):
        module = self.get_object()
        serializer = self.get_serializer(module)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @workspace_permission_by_role(RoleChoices.ADMIN)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    @workspace_permission_by_role(RoleChoices.ADMIN)
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @workspace_permission_by_role(RoleChoices.ADMIN)
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
