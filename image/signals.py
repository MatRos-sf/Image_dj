from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from PIL import Image as PillowImage
from random import randint
from .models import Image, Gallery
import os

def rename_path(path, suffix):

    directory, filename = os.path.split(path)
    name, ext = os.path.splitext(filename)

    return os.path.join(directory, f"{suffix}__{name}{ext}")


@receiver(post_save, sender=Image)
def create_images(sender, instance, created, **kwargs):
    if created:
        if instance.is_original:

            # check tier
            user_tier = instance.profile.profile_tier
            image_sizes = [size.size for size in user_tier.thumbnail_sizes.all()]

            # create thumbnail
            original_image_path = instance.image.path

            # create Gallery
            gallery = Gallery.objects.create(name=f"{instance.pk}", author=instance.profile)
            # add modeel Gallery to Image
            instance.gallery = gallery

            for index, size in enumerate(image_sizes):

                img = PillowImage.open(original_image_path)
                img = img.resize((size, size))

                new_name= rename_path(original_image_path, str(size))
                img.save(new_name)

                directory, filename = os.path.split(new_name)
                # create models following by rules
                if not user_tier.original_file and index == 0:

                    currently = instance
                    currently.image = f"{instance.profile.pk}/{filename}"
                    currently.save()

                    # old file remove because we don't need original
                    os.remove(original_image_path)

                else:
                    Image.objects.create(profile=instance.profile, image=f"{instance.profile.pk}/{filename}",
                                         is_original=False, gallery=gallery)

            # create binary image
            if not instance.expiry:
                expiry = randint(300, 30000)
            else:
                expiry = instance.expiry
            ## I'm not sure!

            if instance.binary_permission:
                img = PillowImage.open(original_image_path)
                binary_image = img.convert('1')
                new_name= rename_path(original_image_path, 'binary')

                binary_image.save(new_name)
                directory, filename = os.path.split(new_name)
                Image.objects.create(profile=instance.profile, image=f"{instance.profile.pk}/{filename}",
                                     expiry=expiry, is_original=False, gallery=gallery)

            # instance.expiry = None because only binary Image need expiry
            instance.expiry = None
            instance.save()
    else:
        # when we edit binary file
        if not instance.is_active and instance.expiry and instance.profile.user.is_superuser:
            instance.is_active = True
            # new date
            instance.created = timezone.now()
            instance.save()