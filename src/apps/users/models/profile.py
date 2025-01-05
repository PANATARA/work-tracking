from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        to='users.User', 
        on_delete=models.CASCADE, 
        related_name='profile',
        verbose_name='User'
    )
    bio = models.TextField(
        verbose_name='About me', 
        null=True, 
        blank=True
    )
    telegram_id = models.CharField(
        max_length=20, 
        verbose_name='Telegram ID', 
        null=True, 
        blank=True
    )
    github = models.URLField(
        verbose_name='GitHub profile', 
        null=True, 
        blank=True
    )
    linkedin = models.URLField(
        verbose_name='LinkedIn profile', 
        null=True, 
        blank=True
    )
    company = models.CharField(
        max_length=100, 
        verbose_name='Company', 
        null=True, 
        blank=True
    )
    position = models.CharField(
        max_length=100, 
        verbose_name='Position', 
        null=True, 
        blank=True
    )
    location = models.CharField(
        max_length=100, 
        verbose_name='Location', 
        null=True, 
        blank=True
    )
    
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    def __str__(self):
        return f'{self.user} ({self.pk})'\


