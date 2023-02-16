from django.db import models

class ThumbnailSize(models.Model):

    size = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return str(self.size)

class ProfileTier(models.Model):

    name = models.CharField(max_length=100)
    thumbnail_sizes = models.ManyToManyField(ThumbnailSize)
    original_file = models.BooleanField()
    binary_file = models.BooleanField()

    def __str__(self):
        return self.name
