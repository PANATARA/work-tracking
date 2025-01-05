from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from apps.users.models.profile import Profile
from apps.users.models.users import User
from apps.users.models.users_settings import UserSettings


class ProfileAdmin(admin.StackedInline):
    model = Profile
    fieldsets = (
        (None, {"fields": ("bio", "location", "position", "company")}),
        (
            _("Social media"),
            {
                "fields": (
                    "telegram_id",
                    "github",
                    "linkedin",
                )
            },
        ),
    )


class UserSettingsAdmin(admin.StackedInline):
    model = UserSettings
    fields = (
        "last_workspace_id",
        "app_theme",
        "language",
        "mention",
        "auto_subsсribe_to_task",
    )


@admin.register(User)
class UserAdmin(UserAdmin):
    change_user_password_template = None
    fieldsets = (
        (None, {"fields": ("phone_number", "email", "username")}),
        (
            _("Личная информация"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "last_request")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "phone_number",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    list_display = (
        "id",
        "username",
        "full_name",
        "email",
        "phone_number",
    )
    list_display_links = (
        "id",
        "username",
    )
    list_filter = (
        "is_staff", 
        "is_superuser", 
        "is_active", 
        "groups"
    )
    search_fields = (
        "id",
        "username",
        "first_name",
        "last_name",
        "email",
        "phone_number",
    )
    ordering = ("-id",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    readonly_fields = (
        "last_login", 
        "last_request"
    )
    inlines = (
        ProfileAdmin,
        UserSettingsAdmin,
    )
