from django.db import models


class TaskTag(models.Model):
    name = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="Tag", 
        db_index=True,
    )

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self) -> str:
        return f"ID:{self.id} {self.name}"
