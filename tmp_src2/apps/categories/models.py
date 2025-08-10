from django.db import models
from tmp_src2.apps.common.models import TimestampedModel


class Category(TimestampedModel):
    """Categories for organizing questions (e.g., Algorithms, Data Structures)"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)  # Icon class name
    color = models.CharField(max_length=7, default='#007bff')  # Hex color
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Tag(TimestampedModel):
    """Tags for more granular categorization (e.g., recursion, dynamic-programming)"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#6c757d')

    def __str__(self):
        return self.name
