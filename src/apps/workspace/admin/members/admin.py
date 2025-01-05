from django.contrib import admin

from apps.workspace.models import workspace_user_config


@admin.register(workspace_user_config.UserFavorite)
class UserFavoriteInline(admin.ModelAdmin):
    list_display = (
        "user",
        "workspace",
        "is_folder",
        "entity_type",
        "entity_identifier",
    )
    search_fields = [
        "user__username",
        "workspace__name",
    ]
    list_filter = [
        "is_folder",
    ]


class FiltersInline(admin.TabularInline):
    model = workspace_user_config.DisplayFilters

    fields = (
        "priority",
        "state",
        "assignee",
        "module",
        "created_by",
    )


class PropertiesInline(admin.TabularInline):
    model = workspace_user_config.DisplayProperties

    fields = (
        "deadline",
        "priority",
        "assignees",
        "state",
        "state_date",
        "module",
        "tags",
    )


@admin.register(workspace_user_config.UserWorkspaceConfig)
class UserConfigAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "workspace",
    )

    inlines = (
        PropertiesInline,
        FiltersInline,
    )

    search_fields = [
        "user__username",
        "workspace__name",
    ]