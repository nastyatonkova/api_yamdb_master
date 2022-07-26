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


class Category(models.Model):
    pass


class Genre(models.Model):
    pass


class Title(models.Model):
    pass


class Reviews(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(
        YaUser, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text


class Comments(models.Model):
    review = models.ForeignKey(
        Reviews, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(
        YaUser, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
