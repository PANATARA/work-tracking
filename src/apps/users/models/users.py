from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from apps.users.managers import CustomUserManager
from django.db import models

from apps.users.models.profile import Profile
from apps.users.models.users_settings import UserSettings


class User(AbstractUser):
    username = models.CharField(
        'Username', 
        max_length=64, 
        unique=True, 
        null=True, 
        blank=True
    )
    email = models.EmailField(
        'Email', 
        unique=True, 
        null=True, 
        blank=True
    )
    phone_number = PhoneNumberField(
        'Phone number', 
        unique=True, 
        null=True, 
        blank=True
    )
    last_request = models.DateTimeField(
        null=True, 
        blank=True
    )
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()


    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_absolute_url(self):
        return reverse('api:users-profile', kwargs={'user_id': self.pk})

    def __str__(self):
        return f"{self.username} (id:{self.pk})"


@receiver(post_save, sender=User)
def post_save_user(sender, instance, created, **kwargs):
    if not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)
    if not hasattr(instance, 'settings'):
        UserSettings.objects.create(user=instance)
