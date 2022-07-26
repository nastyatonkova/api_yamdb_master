from django.db import models
from django.contrib.auth.models import AbstractUser


class YaUser(AbstractUser):
    ADMIN = 1
    MODERATOR = 2
    USER = 3
    ROLE_CHOICES = (
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    )
    role = models.PositiveSmallIntegerField(
        verbose_name='Роль',
        choices=ROLE_CHOICES,
        blank=True,
        null=True,
        default=USER
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Электронная почта'
    )
    username = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        unique=True,
        null=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'email')

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            ),
        ]
