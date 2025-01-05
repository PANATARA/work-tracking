from django.db import models
from datetime import timedelta

from django.urls import reverse
from apps.workspace.constant import ProjectStateChoices, TaskStateChoices
from apps.workspace.models import workspace


class WorkspaceConfiguration(models.Model):
    workspace = models.OneToOneField(
        to=workspace.Workspace, on_delete=models.CASCADE, related_name="configuration"
    )
    archive_completed_task = models.BooleanField(default=True)
    archive_after = models.DurationField(default=timedelta(days=3))

    """Аdd these fields in the future"""
    # workspace_icon = ...

    class Meta:
        indexes = [
            models.Index(fields=["workspace"]),
        ]
        verbose_name = "Workspace configuration"
        verbose_name_plural = "Workspace configuration"
    
    def get_absolute_url(self):
        return reverse(
            "api:workspace-configuration-detail", 
            kwargs={
                "workspace_id": self.workspace.id
            }
        )


class ProjectState(models.Model):
    workspace = models.ForeignKey(
        to=workspace.Workspace, on_delete=models.CASCADE, related_name="projects_states"
    )
    name = models.CharField(max_length=64)
    type = models.SmallIntegerField(
        choices=ProjectStateChoices.CHOICES,
        default=ProjectStateChoices.STARTED,
    )

    class Meta:
        indexes = [
            models.Index(fields=["workspace"]),
        ]
        verbose_name = "Project state"
        verbose_name_plural = "Projects states"
        # unique_together = ("workspace", "name")

    def get_absolute_url(self):
        return reverse(
            "api:workspace-project-states-detail", 
            kwargs={
                "workspace_id": self.workspace.id, 
                "state_id": self.id
            }
        )

    def __str__(self) -> str:
        return f"{self.name}/type:{self.type} | ID:{self.id}"


class TaskState(models.Model):
    workspace = models.ForeignKey(
        to=workspace.Workspace, on_delete=models.CASCADE, related_name="tasks_states"
    )
    name = models.CharField(max_length=64)
    type = models.SmallIntegerField(
        choices=TaskStateChoices.CHOICES,
        default=TaskStateChoices.NOT_STARTED,
    )

    class Meta:
        indexes = [
            models.Index(fields=["workspace"]),
        ]
        verbose_name = "Task state"
        verbose_name_plural = "Tasks states"
        # unique_together = ("workspace", "name")

    def get_absolute_url(self):
        return reverse(
            "api:workspace-task-states-detail", 
            kwargs={
                "workspace_id": self.workspace.id, 
                "state_id": self.id
            }
        )

    def __str__(self) -> str:
        return f"{self.name}/type:{self.type} | ID:{self.id}"
