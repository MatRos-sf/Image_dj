from django.test import TestCase
from django.contrib.auth.models import User

from faker import Faker

from user.models import Profile
from tier.models import ProfileTier

class ModelTest(TestCase):

    def test_create_user_check_signal_default(self):
        User.objects.create_user(username='Test', password='test12345')
        self.assertEqual(Profile.objects.count(), 1)

        # make sure default tier is correct
        tier = Profile.objects.first()
        tier = tier.profile_tier.name
        self.assertTrue(tier, "Basic")

        # make sure default size thumbnails
        thumbnail_size = Profile.objects.first()
        thumbnail_size = thumbnail_size.profile_tier.thumbnail_sizes.first()
        self.assertTrue(200, thumbnail_size.size)

    def test_random_create_user(self):
        fake = Faker()
        users = [fake.simple_profile()['username'] for _ in range(10)]

        # create user
        for user in users:
            User.objects.create_user(username=user, password='1234567')

        # make sure signal
        self.assertTrue(Profile.objects.count(), 10)

        # check different tier
        tier_p = ProfileTier.objects.get(name='Premium')
        tier_e = ProfileTier.objects.get(name='Enterprise')
        for profile in Profile.objects.all():
            if profile.pk > 3 and profile.pk <= 8:
                profile.profile_tier = tier_p
            elif profile.pk > 8:
                profile.profile_tier = tier_e
            profile.save()

        # count tier
        amt_b = Profile.objects.filter(profile_tier__name='Basic').count()
        amt_p = Profile.objects.filter(profile_tier__name='Premium').count()
        amt_e = Profile.objects.filter(profile_tier__name='Enterprise').count()

        self.assertEqual(amt_b,3)
        self.assertEqual(amt_p, 5)
        self.assertEqual(amt_e, 2)

