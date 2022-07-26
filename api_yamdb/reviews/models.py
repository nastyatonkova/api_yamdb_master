from django.db import models
from django.contrib.auth.models import AbstractUser


class YaUser(AbstractUser):
    class RoleChoices(models.TextChoices):
        USER = "user", "user"
        MODERATOR = "moderator", "moderator"
        ADMIN = "admin", "admin"

    is_active = models.BooleanField(default=False)
    email = models.EmailField(max_length=60, unique=True)
    bio = models.CharField(max_length=200, blank=True)
    role = models.CharField(
        max_length=30, choices=RoleChoices.choices, default=RoleChoices.USER
    )
