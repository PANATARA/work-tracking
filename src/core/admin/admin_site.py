from django.contrib import admin
from django.http import HttpRequest

app_order = [
    "users",
    "workspace",
    "projects", 
    "notification", 
    "activitylog", 
    "offers",
]

class AdminSite(admin.AdminSite):

    def get_app_list(self, request: HttpRequest, app_label: str | None = None) -> list[dict]:
        app_list = super().get_app_list(request, app_label)
        app_list.sort(key=self._get_app_order_index)
        return app_list

    @staticmethod
    def _get_app_order_index(element: dict) -> int:

        if element["app_label"] in app_order:
            return app_order.index(element["app_label"])

        return len(app_order)


from django.contrib.admin.apps import AdminConfig

class CustomAdminConfig(AdminConfig):
    default_site = "core.admin.admin_site.AdminSite"