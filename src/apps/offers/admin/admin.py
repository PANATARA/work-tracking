from django.contrib import admin

from core.admin.forms import ImprovedModelForm
from apps.offers.models.offers import Offer


class OfferInline(admin.TabularInline):
    model = Offer

    fields = (
        "user",
        "user_accept",
        "admin_accept",
    )
    extra=0
    classes = ['collapse']


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    form=ImprovedModelForm
    list_display = (
        "id",
        "workspace",
        "user_role",
        "user",
        "status",
        "is_read_by_user",
    )
    readonly_fields = (
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
    )
    search_fields = [
        "id",
        "workspace__name",
        "user__username",
        "message_text",
    ]
    list_filter = [
        "is_read_by_user",
        "user_role",
    ]

    def status(self, obj):
        return obj.status

    status.short_description = "Status"
