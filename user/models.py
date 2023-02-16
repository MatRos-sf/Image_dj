from django.db import models
from django.contrib.auth.models import User

from tier.models import ProfileTier

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_tier = models.ForeignKey(ProfileTier, on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return self.user.username
