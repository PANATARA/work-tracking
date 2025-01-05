from django.contrib import admin
from apps.projects.admin.modules.forms import ModuleAdminForm
from apps.projects.models.modules import Module



@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    form = ModuleAdminForm
    list_display = (
        "id",
        "name",
        "project",
        "status",
        "date_start",
        "date_end",
    )

    readonly_fields = (
        "created_at",
        "created_by",
        "updated_at",
        "updated_by",
    )

    search_fields = [
        "name",
        "project__name",
        "project__workspace__name",
    ]

    list_filter = [
        "status",
    ]