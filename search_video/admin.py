from django.contrib import admin

# Register your models here.
from search_video.models import VideoData, APIKeys


class VideoDataAdmin(admin.ModelAdmin):
    list_display = ['title', 'publisher', 'published_at']


class APIKeysAdmin(admin.ModelAdmin):
    list_display = ['api_key', 'created_at', 'updated_at']


admin.site.register(VideoData, VideoDataAdmin)
admin.site.register(APIKeys)
