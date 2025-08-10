from django.contrib.auth.models import AbstractUser
from django.db import models
from src2.apps.common.models import TimestampedModel


class User(AbstractUser):
    """Custom user model extending Django's AbstractUser"""
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=500, blank=True)
    github_username = models.CharField(max_length=100, blank=True)
    linkedin_profile = models.URLField(blank=True)
    total_points = models.IntegerField(default=0)
    problems_solved = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class UserProfile(TimestampedModel):
    """Extended profile information for users"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    preferred_language = models.CharField(max_length=50, default='python')
    skill_level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
            ('expert', 'Expert')
        ],
        default='beginner'
    )
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    is_public = models.BooleanField(default=True)
