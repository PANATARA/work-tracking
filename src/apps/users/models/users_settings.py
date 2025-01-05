from django.db import models


class UserSettings(models.Model):
    user = models.OneToOneField(
        to='users.User', 
        on_delete=models.CASCADE, 
        related_name='settings',
        verbose_name='User'
    )
    last_workspace_id = models.ForeignKey(
        to="workspace.Workspace",
        on_delete=models.SET_NULL,
        verbose_name="Last openned workspace",
        null=True,
        blank=True,
    )
    app_theme = models.CharField(
        max_length=128,
        default="ExtraDark"
    )
    language = models.CharField(
        max_length=128,
        default="English",
    )

    # Notification preferences
    auto_subsсribe_to_task = models.BooleanField(
        default=True, 
        help_text="Subscribe the user to the tasks that he created or performs"
    )
    mention = models.BooleanField(
        default=True, 
        help_text="Sending a notification when a user is assigned as a task executor"
    )

    #TODO Email-notifications preferences

    class Meta:
        verbose_name = 'User settings'
        verbose_name_plural = 'Users settings'

    def __str__(self):
        return f'{self.user} ({self.pk})'


