from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Case, When, Value

from core.models.mixins import InfoManager, InfoMixin
from apps.workspace.constant import RoleChoices

User = get_user_model()

class OfferManager(InfoManager):
    def get_queryset(self):
        return (
            super().get_queryset().annotate(
                status=Case(
                    When(
                        user_accept__isnull=True,
                        admin_accept=True,
                        then=Value("awaiting_confirmation"),
                    ),
                    When(
                        user_accept__isnull=True,
                        admin_accept=False,
                        then=Value("canceled"),
                    ),
                    When(user_accept=True, admin_accept=True, then=Value("accepted")),
                    When(
                        user_accept=False, admin_accept=True, then=Value("rejected")
                    ),
                    When(
                        user_accept=True, admin_accept=False, then=Value("canceled")
                    ),
                    default=Value("Other status"),
                )
            )
        )

class Offer(InfoMixin):
    workspace = models.ForeignKey(
        to="workspace.Workspace", 
        on_delete=models.SET_NULL, 
        related_name="offers", 
        verbose_name="Workspace",
        null=True,
    )
    admin_accept = models.BooleanField(
        verbose_name="Admin Accept",
        default=True, 
        blank=True,
    )
    user = models.ForeignKey(
        to=User, 
        on_delete=models.SET_NULL, 
        related_name="offers", 
        verbose_name="User",
        null=True,
    )
    user_accept = models.BooleanField(
        verbose_name="User Accept", 
        null=True, 
        blank=True
    )
    user_role = models.SmallIntegerField(
        choices=RoleChoices.CHOICES,
        default=RoleChoices.MEMBER,
        verbose_name="Members role",
    )
    message_text = models.TextField(
        verbose_name="Message text", 
        null=True, 
        blank=True
    )
    is_read_by_user = models.BooleanField(
        default=False
    )

    objects=OfferManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.workspace is None and self.user is None:
            self.delete()

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
        ]
        verbose_name = "Offer"
        verbose_name_plural = "Offers"
        ordering = ("-created_at",)

    def __str__(self):
        return f"Offer №{self.pk}"