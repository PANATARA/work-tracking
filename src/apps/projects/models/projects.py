from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse

from core.models.mixins import StartEndMixin
from apps.workspace.models import workspace, workspace_config
from apps.workspace.validators import all_user_in_workspace, projects_states_in_workspace

User = get_user_model()


class Project(StartEndMixin):
    name = models.CharField(
        verbose_name="Project Name",
        max_length=255,
    )
    manager = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        related_name="managed_projects",
        verbose_name="Manager",
        null=True,
    )
    workspace = models.ForeignKey(
        to=workspace.Workspace,
        on_delete=models.CASCADE,
        related_name="projects",
        blank=False,
    )
    description = models.TextField(
        verbose_name="Description",
        null=True,
        blank=True,
    )
    state = models.ForeignKey(
        to=workspace_config.ProjectState,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    
    def get_absolute_url(self):
        return reverse(
            'api:projects-detail', 
            kwargs={
                'workspace_id': self.workspace.id, 
                "project_id": self.pk
            }
        )

    class Meta:
        indexes = [
            models.Index(fields=["workspace"]),
        ]
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ("name",)

    def __str__(self):
        return f"{self.name} (ID:{self.pk})"
