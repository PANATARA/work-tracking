from django.contrib import admin
from apps.projects.admin.tasks.filters import TaskPriorityFilter, TaskStateFilter
from apps.projects.admin.tasks.forms import TaskAdminForm, TaskInlineAdminForm
from apps.projects.models import tasks


class SubscriberTaskInline(admin.TabularInline):
    model = tasks.TaskSubscriber
    fields = ("subscriber",)
    extra = 1


class TaskInline(admin.TabularInline):
    model = tasks.Task
    fields = ("id", "title", "state", "is_archive",)
    show_change_link = True
    form = TaskInlineAdminForm
    extra = 0


@admin.register(tasks.Task)
class TaskAdmin(admin.ModelAdmin):
    form = TaskAdminForm
    list_display = (
        "id",
        "title",
        "project",
        "module",
        "get_assignees",
        "state",
        "is_archive",
    )
    readonly_fields = (
        "created_at",
        "created_by",
        "updated_at",
        "updated_by",
    )

    list_filter = [
        TaskStateFilter,
        TaskPriorityFilter,
        "is_archive",
    ]

    search_fields = [
        "title",
        "workspace__name",
        "assignees__username",
    ]

    inlines = (SubscriberTaskInline,)

    def get_assignees(self, obj):
        return ", ".join([str(p) for p in obj.assignees.all()])

    get_assignees.short_description = "Assignees"


    def get_queryset(self, request):
        active_tasks = super().get_queryset(request)
        archive_task = self.model.archive_objects.all()
        return active_tasks | archive_task