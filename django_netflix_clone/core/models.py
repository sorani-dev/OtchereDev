import imp
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractUser

AGE_CHOICES = (
    ('All', 'All'),
    ('Kids', 'Kids'),
)

MOVIE_CHOICES = (
    ('seasonal', 'Seasonal'),
    ('single', 'Single'),
)

# Create your models here.


class CustomUser(AbstractUser):
    profiles = models.ManyToManyField('Profile', null=True, blank=True)


class Profile(models.Model):
    name = models.CharField(max_length=225)
    age_limit = models.CharField(max_length=10, choices=AGE_CHOICES)
    uuid = models.UUIDField(default=uuid4)


class Movie(models.Model):
    """Movie."""

    title = models.CharField(max_length=225)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid4)
    type = models.CharField(max_length=10, choices=MOVIE_CHOICES)
    videos = models.ManyToManyField('Video')
    flyer = models.ImageField(uploaded_to='flyers')
    age_limit = models.CharField(max_length=10, choices=AGE)

    class Meta:
        """Meta definition for Movie."""

        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'

    def __str__(self):
        """Unicode representation of Movie."""
        pass


class Video(models.Model):
    """Model definition for Video."""

    title = models.CharField(max_length=225, blank=True, null=True)
    file = models.FileField(upload_to='movies')

    class Meta:
        """Meta definition for Video."""

        verbose_name = 'Video'
        verbose_name_plural = 'Videos'

    def __str__(self):
        """Unicode representation of Video."""
        pass
