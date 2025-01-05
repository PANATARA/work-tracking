from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from apps.workspace.models import workspace

User = get_user_model()


class Notification(models.Model):


    class NotificationTypeChoices(models.IntegerChoices):
        INFORMATIVE = 1, "Informative"
        ATTENTION = 2, "Attention"
        CRITICAL = 3, "Critical"

    workspace = models.ForeignKey(
        to=workspace.Workspace,
        on_delete=models.CASCADE,
        related_name="notifications",
        null=False,
        blank=False,
        verbose_name="Workspace",
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name="User's notifications",
        null=False,
        blank=False,
    )
    triggered_by = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="triggered_notifications",
        verbose_name="Triggered by",
        null=True,
        blank=True,
    )
    entity_type = models.CharField(
        max_length=100,
        null=True, 
        blank=True,
    )
    entity_identifier = models.PositiveIntegerField(
        null=True, 
        blank=True,
    )
    type = models.IntegerField(
        choices=NotificationTypeChoices.choices, 
        default=NotificationTypeChoices.INFORMATIVE
    )
    is_read = models.BooleanField(
        default=False
    )
    message = models.TextField(
        max_length=512,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        verbose_name="Created at", 
        null=True, 
        blank=False
    )

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        if not self.pk and not self.created_at:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            models.Index(fields=["workspace", "user"]),
            models.Index(fields=["user"]),
        ]
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ("-created_at",)

    def __str__(self):
        return f"Notification to the {self.user} from the entity {self.entity_type}"