from django.contrib import admin

from apps.activitylog import models


@admin.register(models.TaskActivityLog)
class TaskLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "task",
        "action_type",
        "field",
        "value",
        "timestamp",
    )

    readonly_fields = (
        "project",
        "workspace",
        "user",
        "task",
        "action_type",
        "field",
        "value",
        "timestamp",
    )

    search_fields = [
        "id",
        "user__username",
        "project__name",
        "workspace__name",
        "task__id",
    ]
    list_filter = [
        "action_type",
        "field",
    ]
