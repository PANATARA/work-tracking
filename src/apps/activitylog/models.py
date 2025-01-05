from django.db import models
from django.contrib.auth import get_user_model

from apps.activitylog.constants import ACTION_CHOICE_TASK
from apps.projects.models import tasks, projects
from apps.workspace.models import workspace

User = get_user_model()


class TaskActivityLog(models.Model):
    project = models.ForeignKey(
        to=projects.Project,
        on_delete=models.CASCADE,
        related_name="tasks_activity",
        verbose_name="Project",
    )
    workspace = models.ForeignKey(
        to=workspace.Workspace,
        on_delete=models.CASCADE,
        related_name="tasks_activity",
        null=False,
        blank=False,
        verbose_name="Workspace",
    )
    task = models.ForeignKey(
        tasks.Task,
        on_delete=models.CASCADE,
        related_name="logs",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )
    action_type = models.CharField(
        max_length=50, choices=ACTION_CHOICE_TASK, blank=False, null=False
    )
    field = models.CharField(max_length=100)
    value = models.CharField(max_length=100, blank=True, null=True)
    detail = models.CharField(max_length=255)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"Log {self.pk}"

    class Meta:
        indexes = [
            models.Index(fields=["task"]),
            models.Index(fields=["user"]),
        ]
        verbose_name = "Task Log"
        verbose_name_plural = "Tasks Logs"
        ordering = ["-timestamp"]
