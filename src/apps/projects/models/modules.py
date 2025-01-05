from django.db import models
from django.urls import reverse

from core.models.mixins import StartEndMixin
from apps.projects.constants import ModuleChoice
from apps.projects.models import projects


class Module(StartEndMixin):
    workspace = models.ForeignKey(
        to="workspace.Workspace",
        on_delete=models.CASCADE,
        related_name="modules",
        blank=False,
    )
    project = models.ForeignKey(
        to=projects.Project, 
        on_delete=models.CASCADE, 
        related_name="modules", 
        verbose_name="Project",
    )
    name = models.TextField(
        verbose_name="Name", 
        max_length=255, 
        null=True, 
        blank=True,
    )
    description = models.TextField(
        verbose_name="Description", 
        null=True, 
        blank=True
    )
    goal = models.TextField(
        verbose_name="Module Goal", 
        null=True, 
        blank=True
    )
    status = models.SmallIntegerField(
        choices=ModuleChoice.CHOICES,
        default=ModuleChoice.IN_BACKLOG,
        verbose_name="Module status",
    )

    class Meta:
        indexes = [
            models.Index(fields=["project"]),
        ]
        verbose_name = "Module"
        verbose_name_plural = "Modules"

    def __str__(self):
        return f"{self.name if self.name else ''} Module (ID:{self.pk})"

    def save(self, *args, **kwargs):
        if not self.name:
            if self.date_start and self.date_end:
                self.name = f"Module {self.date_start.strftime('%d.%m')}-{self.date_end.strftime('%d.%m')}"
            else:
                self.name = "Module"
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse(
            "api:project-modules-detail", 
            kwargs={
                "workspace_id": self.workspace.id, 
                "project_id": self.project.id,
                "module_id": self.id,
            }
        )
