from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

from datetime import timedelta

from user.models import Profile


class Gallery(models.Model):
    name = models.CharField(max_length=100, null=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)

def get_upload_path(instance, filename):
    return f"{instance.profile.pk}/{filename}"

class Image(models.Model):

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_upload_path)
    expiry = models.PositiveIntegerField(null=True, validators=[MinValueValidator(300), MaxValueValidator(30000)])

    is_original = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, null=True, blank=True, related_name='images')

    @property
    def get_profile_name(self):
        return self.profile.user.username

    @property
    def get_profile_tier(self):
        return self.profile.profile_tier.name

    @property
    def binary_permission(self):
        return bool(self.profile.profile_tier.binary_file)

    @property
    def link_active(self):
        if not self.expiry:     return True
        date_now = timezone.now()
        date_expiry = self.created + timedelta(seconds= self.expiry)
        if self.is_active and date_expiry < date_now:
            self.is_active = False
            self.expiry = None
            self.save()
        return bool(date_expiry > date_now)


    def __str__(self):
        return f"{self.get_profile_name}__{self.get_profile_tier}: {self.id}"

    def clean(self):
        super(Image, self).clean()
        if self.expiry is not None and (self.expiry < 300 or self.expiry > 30000):
            raise ValidationError('Expiry value must be between 300 and 30000')
