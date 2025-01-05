from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.projects"

    def ready(self) -> None:
        from apps.projects.signals import tasks_signals
        return super().ready()
