from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    LANGUAGES = [
        ('uz', "O'zbekcha"),
        ('ru', "Русский"),
        ('en', "English"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    language = models.CharField(max_length=2, choices=LANGUAGES, default='uz')
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.jpg', blank=True)
    preferred_currency = models.CharField(max_length=3, default='UZS')

    def __str__(self):
        return f"{self.user.username} profili"