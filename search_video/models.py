from datetime import datetime

from django.contrib.postgres.search import SearchVectorField
from django.db import models


# Create your models here.
class VideoData(models.Model):
    video_id = models.CharField(max_length=255, unique=True, null=False, blank=False)
    title = models.TextField()
    description = models.TextField()
    publisher = models.CharField(max_length=255)
    published_at = models.DateTimeField()
    thumbnail_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    search_vector = SearchVectorField(null=True)

    class Meta:
        ordering = ['-published_at']

    def clean_fields(self, exclude=None):
        self.published_at = datetime.fromisoformat(self.published_at)


class APIKeys(models.Model):
    api_key = models.CharField(max_length=255, unique=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
