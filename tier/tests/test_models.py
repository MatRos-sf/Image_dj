from django.test import TestCase

from random import randint

from tier.models import ThumbnailSize, ProfileTier



class ThumbnailSizeTests(TestCase):

    def test_create_thumbnailsize(self):
        random_size = [ randint(1,1000) for i in range(10) ]
        for size in random_size:
            ThumbnailSize.objects.create(size=size)

        self.assertEqual(ThumbnailSize.objects.count(), 10)
        self.assertEqual(ThumbnailSize.objects.first().size, random_size[0])
        self.assertEqual(ThumbnailSize.objects.last().size, random_size[-1])

class ProfileTierTests(TestCase):

    def setUp(self) -> None:
        self.thumbnail_size = ThumbnailSize.objects.create(size=100)
        self.thumbnail_size_2 = ThumbnailSize.objects.create(size=200)

    def test_create_model(self):
        ProfileTier.objects.create(
            name = 'Test',
            original_file = True,
            binary_file = True
        )

        self.assertEqual(ProfileTier.objects.count(), 1)

    def test_create_model_with_thumbnails(self):

        obj = ProfileTier.objects.create(
            name = 'Test',
            original_file = True,
            binary_file = True,
        )
        obj.thumbnail_sizes.add(self.thumbnail_size, self.thumbnail_size_2)
        obj.save()

        thumbnails = obj.thumbnail_sizes.count()
        self.assertEqual(thumbnails, 2)