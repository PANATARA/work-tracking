from django.contrib import admin

from core.admin.forms import ImprovedModelForm
from apps.notification.models.notification import Notification


@admin.register(Notification)
class OfferAdmin(admin.ModelAdmin):
    form = ImprovedModelForm
    list_display = (
        "id",
        "user",
        "triggered_by",
        "entity_type",
        "entity_identifier",
        "message",
        "is_read",
    )
    readonly_fields = (
        "entity_type",
        "entity_identifier",
        "created_at",
    )
    list_filter = [
        "is_read",
        "entity_type",
    ]
    search_fields = [
        "user__username",
        "entity_type",
        "entity_identifier",
        "triggered_by__username",
    ]
