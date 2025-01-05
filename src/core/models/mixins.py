from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from crum import get_current_user

User = get_user_model()


class InfoManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().select_related(
                "created_by__user_avatar",
                "updated_by__user_avatar"
            )
        )


class DateMixin(models.Model):
    created_at = models.DateTimeField("Created at", null=True, blank=False)
    updated_at = models.DateTimeField("Updated at", null=True, blank=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        if not self.pk and not self.created_at:
            self.created_at = timezone.now()

        update_fields = kwargs.get("update_fields", None)
        if update_fields:
            if "updated_at" not in update_fields:
                update_fields.append("updated_at")
            kwargs["update_fields"] = update_fields

        return super(DateMixin, self).save(*args, **kwargs)


class InfoMixin(DateMixin):
    created_by = models.ForeignKey(
        User,
        models.SET_NULL,
        "created_%(app_label)s_%(class)s",
        verbose_name="Created by",
        null=True,
    )
    updated_by = models.ForeignKey(
        User,
        models.SET_NULL,
        "updated_%(app_label)s_%(class)s",
        verbose_name="Updated by",
        null=True,
    )

    objects = InfoManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.updated_by = user
        update_fields = kwargs.get("update_fields", None)

        if update_fields:
            if "updated_by" not in update_fields:
                update_fields.append("updated_by")
            kwargs["update_fields"] = update_fields

        super().save(*args, **kwargs)


class StartEndMixin(InfoMixin):
    date_start = models.DateTimeField("Start date", null=True, blank=True)
    date_end = models.DateTimeField("End date", null=True, blank=True)

    class Meta:
        abstract = True
