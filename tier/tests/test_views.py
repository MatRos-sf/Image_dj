from django.test import TestCase, Client
from django.shortcuts import reverse

from tier.models import ProfileTier, ThumbnailSize

class ViewsTest(TestCase):

    def test_create_default_profile_tier(self):
        c = Client()
        response = c.get(reverse('set_website'))

        # make sure the response is successful
        self.assertTrue(response.status_code, 201)


        amt_profile_tier = ProfileTier.objects.count()
        amt_thumbnail_size = ThumbnailSize.objects.count()

        # make sure the corect number of ProfileTier, ThumbnailSize
        self.assertEqual(amt_profile_tier, 3)
        self.assertEqual(amt_thumbnail_size, 2)

        # make sure last and first model ProfielTier
        first = ProfileTier.objects.first()
        last = ProfileTier.objects.last()

        self.assertEqual(last.name, "Enterprise")
        self.assertEqual(first.name, "Basic")

    def test_create_default_profile_tier_done(self):

        c = Client()
        response = c.get(reverse('set_website'))

        # make sure the response is successful
        self.assertTrue(response.status_code, 201)

        response = c.get(reverse('set_website'))

        self.assertEqual(response.status_code, 410)