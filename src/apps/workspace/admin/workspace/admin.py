from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.db.models import Count, Q
from django.http import HttpRequest

from apps.offers.admin.admin import OfferInline
from apps.workspace.admin.workspace.filters import TotalMembersFilter, TotalProjectsFilter
from apps.workspace.admin.workspace.forms import WorkspaceAdminForm, WorkspaceMemberInlineAdminForm
from apps.workspace.constant import RoleChoices
from apps.workspace.models import workspace, workspace_config
from apps.projects.admin.projects.admin import ProjectInline


class WorkspaceMemberInline(admin.TabularInline):
    model = workspace.WorkspaceMember
    # form = WorkspaceMemberInlineAdminForm

    fields = (
        "user",
        "role",
        "date_joined",
    )
    extra = 0
    readonly_fields = ["date_joined"]


class WorkspaceConfigurationInline(admin.TabularInline):
    model = workspace_config.WorkspaceConfiguration

    fields = (
        "archive_completed_task",
        "archive_after",
    )


class ProjectStateInline(admin.TabularInline):
    model = workspace_config.ProjectState

    fields = (
        "name",
        "type",
    )
    extra=0
    classes = ['collapse']


class TaskStateInline(admin.TabularInline):
    model = workspace_config.TaskState

    fields = (
        "name",
        "type",
    )
    extra=0
    classes = ['collapse']


@admin.register(workspace.Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    form=WorkspaceAdminForm
    list_display = (
        "id",
        "name",
        "owner",
        "total_projects",
        "total_members",
        "total_active_tasks",
        "total_archived_tasks",
    )

    readonly_fields = (
        "created_at",
        "created_by",
        "updated_at",
        "updated_by",
    )

    inlines = (
        WorkspaceMemberInline,
        WorkspaceConfigurationInline,
        ProjectInline,
        ProjectStateInline,
        TaskStateInline,
        OfferInline,
    )

    search_fields = [
        "id",
        "name",
        "owner__username",
    ]

    list_filter = [
        TotalMembersFilter,
        TotalProjectsFilter,
    ]

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return workspace.Workspace.objects.annotate(
                total_members=Count("members", distinct=True),
                total_active_tasks=Count("tasks", distinct=True, filter=Q(tasks__is_archive=False)),
                total_archived_tasks=Count("tasks", distinct=True, filter=Q(tasks__is_archive=True)),
                total_projects = Count("projects", distinct=True),
            ).select_related(
                "owner",
            ).prefetch_related(
                "members",
            )

    def total_members(self, obj):
        return obj.total_members

    def total_active_tasks(self, obj):
        return obj.total_active_tasks

    def total_archived_tasks(self, obj):
        return obj.total_archived_tasks

    def total_projects(self, obj):
        return obj.total_projects

    total_members.admin_order_field = 'total_members'  
    total_members.short_description = "Total members"  
    total_active_tasks.admin_order_field = 'total_active_tasks'  
    total_active_tasks.short_description = "Total active tasks"
    total_archived_tasks.admin_order_field = 'total_archived_tasks'  
    total_archived_tasks.short_description = "Total archived tasks"
    total_projects.admin_order_field = 'total_projects'
    total_projects.short_description = "Total projects"

@admin.register(workspace_config.TaskState)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "type",
        "workspace",
    ]