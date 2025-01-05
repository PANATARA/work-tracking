from django.contrib import admin

from core.models.image_keeper import ImageKeeper


@admin.register(ImageKeeper)
class ImageKeeperAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "workspace",
        "task",
        "size",
        "is_archived",
    )

    readonly_fields = (
        "size",
        "created_by",
        "updated_by",
        "updated_at",
        "created_at",
    )
