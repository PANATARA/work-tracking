from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone

from core.models.mixins import InfoMixin
from apps.workspace.constant import RoleChoices

User = get_user_model()


class Workspace(InfoMixin):
    name = models.CharField(
        verbose_name="Workspace Name",
        max_length=255,
        blank=False,
    )
    description = models.TextField(
        verbose_name="Description",
        null=True,
        blank=True,
    )
    slug = models.SlugField(blank=True)
    owner = models.ForeignKey(
        to=User,
        on_delete=models.RESTRICT,
        related_name="owned_workspaces",
        verbose_name="Owner",
        blank=False,
    )
    members = models.ManyToManyField(
        to=User,
        related_name="member_workspaces",
        verbose_name="Members",
        through="WorkspaceMember",
        blank=True,
    )

    class Meta:
        verbose_name = "Workspace"
        verbose_name_plural = "Workpspaces"
        ordering = ("name",)

    def get_absolute_url(self):
        return reverse(
            "api:workspace-detail", 
            kwargs={
                "workspace_id": self.pk
            }
        )

    def __str__(self):
        return f"{self.name} (ID:{self.pk})"


class WorkspaceMember(models.Model):
    workspace = models.ForeignKey(
        to=Workspace,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="workspace_memberships",
        verbose_name="User",
    )
    date_joined = models.DateField(
        default=timezone.now,
        verbose_name="Date Joined",
    )
    role = models.SmallIntegerField(
        choices=RoleChoices.CHOICES,
        default=RoleChoices.MEMBER,
        verbose_name="Members role",
    )

    class Meta:
        indexes = [
            models.Index(fields=["workspace", "user"]),
            models.Index(fields=["user"]),
        ]
        verbose_name = "Workspace member"
        verbose_name_plural = "Workspace members"
        unique_together = ("workspace", "user")

    def __str__(self) -> str:
        return f"Member ID:{self.id}"
