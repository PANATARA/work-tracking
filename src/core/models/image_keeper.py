import uuid
from django.db import models
from django.core.exceptions import ValidationError

from core.models.mixins import InfoMixin


def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    unique_id = uuid.uuid4().hex
    if instance.user:
        return f"users/avatars/{instance.user.id}_{unique_id}.{ext}"
    elif instance.task:
        return f"tasks/assets/{instance.task.id}_{unique_id}.{ext}"
    return f"unknown/{unique_id}.{ext}"

class ImageKeeper(InfoMixin):
    
    image = models.ImageField(
        verbose_name='Image',
        upload_to=upload_to,
    )
    user = models.OneToOneField(
        to="users.User",
        on_delete=models.CASCADE,
        related_name="user_avatar",
        null=True,
        blank=True,
    )
    workspace = models.OneToOneField(
        to="workspace.Workspace",
        on_delete=models.CASCADE,
        related_name="workspace_avatar",
        null=True,
        blank=True,
    )
    task = models.ForeignKey(
        to="projects.Task",
        on_delete=models.CASCADE,
        related_name="assets",
        null=True,
        blank=True,
    )
    #comment = models.ForeignKey()

    size = models.FloatField(default=0)
    is_archived = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
        ordering = ("-created_at",)
    
    def __str__(self) -> str:
        return super().__str__()
    
    def save(self, *args, **kwargs):
        if not self.user and not self.task:
            raise ValidationError("Image must be linked to either a user or a task.")
        return super().save(*args, **kwargs)
    
    def clean(self):
        super().clean()
        max_size_mb = 5
        if self.image and self.image.size > max_size_mb * 1024 * 1024:
            raise ValidationError(f"File too large. Size should not exceed {max_size_mb}.")
