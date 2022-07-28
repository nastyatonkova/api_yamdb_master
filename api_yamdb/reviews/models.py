from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

from .validators import validate_year, validate_username


USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLE_CHOICES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR)
]


class YaUser(AbstractUser):
    username = models.CharField(
        max_length=150,
        verbose_name='User name',
        validators=(validate_username,),
        unique=True,
        blank=False,
        null=False,
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='User email address',
        unique=True,
        blank=False,
        null=False,
    )
    role = models.CharField(
        max_length=20,
        verbose_name='User role',
        choices=ROLE_CHOICES,
        default=USER
    )
    first_name = models.CharField(
        max_length=50,
        verbose_name='User first name',
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name='User last name',
        blank=True,
        null=True,
    )
    bio = models.TextField(
        verbose_name='About the user',
        max_length=500,
        blank=True,
        null=True
    )
    confirmation_code = models.CharField(
        max_length=255,
        verbose_name='Confirmation code',
        blank=False,
        null=True,
        default='XXXX',
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def is_user(self):
        return self.role == USER
    
    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_admin(self):
        return self.role == ADMIN

    def __str__(self):
        return self.username


@receiver(post_save, sender=YaUser)
def post_save(sender, instance, created, **kwargs):
    if created:
        confirmation_code = default_token_generator.make_token(
            instance
        )
        instance.confirmation_code = confirmation_code
        instance.save()


class Category(models.Model):
    name = models.CharField(
        'Category',
        max_length=200
    )
    slug = models.SlugField(
        'Slug category',
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
        'Genre',
        max_length=200
    )
    slug = models.SlugField(
        'Slug genre',
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
        'Title',
        max_length=200,
        db_index=True
    )
    year = models.IntegerField(
        'Year',
        validators=(validate_year, )
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Category',
        null=True,
        blank=True
    )
    description = models.TextField(
        'Description',
        max_length=255,
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Genre'
    )
    #rating = models.DecimalField(
    #    max_digits=4,
    #    decimal_places=2,
    #    null=True,
    #    default=0,
    #    validators=[
    #        MaxValueValidator(10.00),
    #        MinValueValidator(0)
    #    ])

    class Meta:
        verbose_name = 'Art work'
        verbose_name_plural = 'Art works'

    def __str__(self):
        return self.name


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
