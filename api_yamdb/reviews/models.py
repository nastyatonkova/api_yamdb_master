from django.db import models
from django.contrib.auth.models import AbstractUser

from .validators import validate_year


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
    name = models.CharField(
        'category',
        max_length=200
    )
    slug = models.SlugField(
        'slug category',
        unique=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'{self.name} {self.name}'


class Genre(models.Model):
    name = models.CharField(
        'genre',
        max_length=200
    )
    slug = models.SlugField(
        'slug genre',
        unique=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genries'

    def __str__(self):
        return f'{self.name} {self.name}'


class Title(models.Model):
    name = models.CharField(
        'title',
        max_length=200,
        db_index=True
    )
    year = models.IntegerField(
        'year',
        validators=(validate_year, )
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='category',
        null=True,
        blank=True
    )
    description = models.TextField(
        'description',
        max_length=255,
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='genre'
    )

    class Meta:
        verbose_name = 'Art work'
        verbose_name_plural = 'Art works'

    def __str__(self):
        return self.name
