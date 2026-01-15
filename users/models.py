from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    LANGUAGE_CHOICES = [
        ('uz', "O'zbekcha"),
        ('ru', "Русский"),
        ('en', "English"),
    ]
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='uz')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg')
    def __str__(self):
        return f"{self.user.username} profili"