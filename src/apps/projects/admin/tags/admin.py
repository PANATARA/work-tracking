from django.contrib import admin
from apps.projects.models.tags import TaskTag 


@admin.register(TaskTag)
class TagAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]

    search_fields = [
        "name",
    ]