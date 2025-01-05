from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from core.models.mixins import InfoManager, InfoMixin
from apps.projects.models import modules, projects, tags
from apps.workspace.models import workspace, workspace_config
from apps.workspace.validators import all_user_in_workspace, tasks_states_in_workspace
from apps.workspace.constant import TaskStateChoices

User = get_user_model()


class ActiveTaskManager(InfoManager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                is_archive=False,
            )
        )


class ArchiveTaskManager(InfoManager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                is_archive=True,
            )
        )


class Task(InfoMixin):
    project = models.ForeignKey(
        to=projects.Project,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name="Project",
    )
    module = models.ForeignKey(
        to=modules.Module,
        on_delete=models.SET_NULL,
        related_name="tasks",
        null=True,
        blank=True,
        default=None,
        verbose_name="Module",
    )
    workspace = models.ForeignKey(
        to=workspace.Workspace,
        on_delete=models.CASCADE,
        related_name="tasks",
        null=False,
        blank=False,
        verbose_name="Workspace",
    )
    title = models.CharField(
        verbose_name="Task title",
        default="Task",
    )
    description = models.TextField(
        verbose_name="Task description",
        null=True,
        blank=True,
    )
    assignees = models.ManyToManyField(
        to=User,
        related_name="assigned_tasks",
        verbose_name="Assignees",
        blank=True,
    )
    tags = models.ManyToManyField(
        to=tags.TaskTag,
        verbose_name="Tag",
        blank=True,
    )
    state = models.ForeignKey(
        to=workspace_config.TaskState,
        on_delete=models.SET_NULL,
        related_name="tasks",
        null=True,
        blank=True,
        verbose_name="Task state",
    )
    priority = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        default=1,
        blank=True,
        null=True,
    )
    deadline = models.DateTimeField(verbose_name="Deadline", null=True, blank=True)
    resolution_text = models.TextField(null=True, blank=True)

    # When a task should be archived
    archive_at = models.DateTimeField(
        verbose_name="Archive date",
        null=True,
        blank=True,
    )
    is_archive = models.BooleanField(default=False)

    # Default manager | To work with active tasks
    objects = ActiveTaskManager()

    # To work with archived tasks
    archive_objects = ArchiveTaskManager()

    class Meta:
        indexes = [
            models.Index(fields=["workspace", "project"]),
            models.Index(fields=["project"]),
        ]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Task (ID:{self.pk})"

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def clean(self):
        if self._state.adding and self.project.workspace != self.workspace:
            raise ValidationError("The project does not belong to this workspace")
    
        if self.module and self.module.project != self.project:
            raise ValidationError("The module does not belong to this project")
    def get_absolute_url(self):
        urlname = "api:project-archived-task-detail" if self.is_archive else "api:project-task-detail"
        return reverse(
            urlname, 
            kwargs={
                'workspace_id': self.workspace.id, 
                "project_id": self.project.id,
                "task_id": self.pk,
            }
        )


class TaskSubscriber(models.Model):

    task = models.ForeignKey(
        to=Task,
        on_delete=models.CASCADE,
        verbose_name="Task",
        related_name="task_subscribers",
    )
    subscriber = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        verbose_name="User",
        related_name="task_subscribers",
    )
    workspace = models.ForeignKey(
        to=workspace.Workspace,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Workspace",
    )

    def save(self, *args, **kwargs):
        if not self.pk and not self.workspace:
            self.workspace = self.task.workspace
        if not all_user_in_workspace([self.subscriber.id], self.task.workspace):
            raise ValidationError("There is no such user in this workspace")

        return super().save(*args, **kwargs)

    class Meta:
        unique_together = ["task", "subscriber"]
        verbose_name = "Task Subscriber"
        verbose_name_plural = "Task Subscribers"
