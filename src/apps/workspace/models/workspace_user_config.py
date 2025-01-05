from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from apps.workspace.constant import LayoutChoices, OrderChoices, GroupChoices
from apps.workspace.models import workspace_config as wpc
from apps.workspace.validators import all_user_in_workspace
from . import workspace

User = get_user_model()


class UserWorkspaceConfig(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        db_index=True,
    )
    workspace = models.ForeignKey(
        to=workspace.Workspace,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        db_index=True,
    )
    layout = models.CharField(
        max_length=64,
        choices=LayoutChoices.CHOICES,
        default=LayoutChoices.BOARD,
    )
    order_by = models.CharField(
        max_length=64,
        choices=OrderChoices.CHOICES,
        default=OrderChoices.CREATED_AT,
    )
    group_by = models.CharField(
        max_length=64,
        choices=GroupChoices.CHOICES,
        default=GroupChoices.STATE,
    )
    show_empty_groups = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not all_user_in_workspace([self.user], self.workspace):
            raise ValidationError("The user does not belong to this workspace")

        return super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=["workspace", "user"]),
            models.Index(fields=["user"]),
        ]
        verbose_name = "User preferences"
        verbose_name_plural = "Users preferences"
        unique_together = ('user', 'workspace')


def default_priority():
    return {"1": True,"2": True,"3": True}


class DisplayFilters(models.Model):
    user_workspace_config = models.OneToOneField(
        to=UserWorkspaceConfig,
        on_delete=models.CASCADE,
        related_name='filters',
        null=True,
    )
    priority = models.JSONField(
        default=default_priority
    )
    state = models.ManyToManyField(
        to=wpc.TaskState,
        blank=True,
    )
    assignee = models.ManyToManyField(
        to=User,
        blank=True,
        related_name="filter_assignee"
    )
    module = models.ManyToManyField(
        to='projects.Module',
        blank=True,
    )
    created_by = models.ManyToManyField(
        to=User,
        blank=True,
    )

    class Meta:
        verbose_name = "Display filter"
        verbose_name_plural = "Display filters"


class DisplayProperties(models.Model):
    user_workspace_config = models.OneToOneField(
        to=UserWorkspaceConfig,
        on_delete=models.CASCADE,
        related_name='properties',
        null=True,
    )
    deadline = models.BooleanField(default=True)
    priority = models.BooleanField(default=True)
    assignees = models.BooleanField(default=True)
    state = models.BooleanField(default=True)
    module = models.BooleanField(default=True)
    state_date = models.BooleanField(default=True)
    tags = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Display propetry"
        verbose_name_plural = "Display properties"


class UserFavorite(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        db_index=True,
    )
    workspace = models.ForeignKey(
        to=workspace.Workspace,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        db_index=True,
    )
    is_folder = models.BooleanField()
    name = models.CharField()
    entity_type = models.CharField(max_length=100, null=True, blank=True)
    entity_identifier = models.PositiveBigIntegerField(null=True, blank=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="parent_folder",
    )
    sequence = models.FloatField(default=65535)

    class Meta:
        unique_together = [
            "entity_type",
            "user",
            "entity_identifier",
        ]
        verbose_name = "User Favorite"
        verbose_name_plural = "User Favorites"

    def save(self, *args, **kwargs):
        if self._state.adding:
            largest_sequence = UserFavorite.objects.filter(
                workspace=self.workspace,
                user=self.user
            ).aggregate(
                largest=models.Max("sequence")
            )["largest"]
            if largest_sequence is not None:
                self.sequence = largest_sequence + 10000

        super(UserFavorite, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} <{self.entity_type}>"