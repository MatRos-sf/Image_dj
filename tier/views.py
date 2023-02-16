from django.shortcuts import HttpResponse
from django.http import HttpResponseGone

from .models import ThumbnailSize, ProfileTier
def create_profile_tier():
    import json
    import os
    from django.conf import settings

    # create default ThumbnailSize
    size_200 = ThumbnailSize.objects.create(size=200)
    size_400 = ThumbnailSize.objects.create(size=400)

    # create ProfileTier
    with open(os.path.join(settings.BASE_DIR, 'static', 'default_profile_tier.json')) as f:
        payload = json.loads(f.read())

    for date in payload:
        tier = ProfileTier.objects.create(**date)
        if date['name'] == 'Basic':
            tier.thumbnail_sizes.add(size_200)
        else:
            tier.thumbnail_sizes.add(size_200, size_400)
        tier.save()


def create_default_profile_tier_view(request):
    """
    It's a simple function who creates three default models
    """
    if ProfileTier.objects.count() == 0:
        create_profile_tier()
        return HttpResponse('<h1>Created three dafault tier: Basic, Premium, Enterprise</h1>', status=201)
    else:
        return HttpResponseGone('Link is invalid.')

