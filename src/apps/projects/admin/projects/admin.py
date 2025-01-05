from django.contrib import admin
from apps.projects.admin.projects.filters import ProjectStateFilter
from apps.projects.admin.projects.forms import ProjectAdminForm
from apps.projects.admin.tasks.admin import TaskInline
from apps.projects.models import projects

class ProjectInline(admin.TabularInline):
    model = projects.Project
    form = ProjectAdminForm
    fields = (
        "id", 
        "name", 
        "state", 
        "manager"
    )
    extra=0

@admin.register(projects.Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectAdminForm
    list_display = (
        "id",
        "name",
        "manager",
        "state",
        "workspace",
    )

    readonly_fields = (
        "created_at",
        "created_by",
        "updated_at",
        "updated_by",
    )

    list_filter = [
        ProjectStateFilter,
    ]

    search_fields = [
        "name",
        "manager__username",
        "workspace__name",
    ]

    inlines = (
        TaskInline,
    )

    def get_queryset(self, request):
        return super().get_queryset(request)