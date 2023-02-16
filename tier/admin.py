from django.contrib import admin

from .models import ThumbnailSize, ProfileTier

admin.site.register(ProfileTier)
admin.site.register(ThumbnailSize)