from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


from .models import Profile
from tier.views import create_profile_tier
from tier.models import ProfileTier

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        p = Profile.objects.create(user=instance)
        # check ProfileTier exist
        try:
            obj = ProfileTier.objects.get(id=1)
        except ObjectDoesNotExist:
            create_profile_tier()
            obj = ProfileTier.objects.get(id=1)
        # set default profile_tier
        p.profile_tier = obj
        p.save()


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
