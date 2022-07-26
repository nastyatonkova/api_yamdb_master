from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .validators import validate_year


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


class Reviews(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(
        YaUser, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ])
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
