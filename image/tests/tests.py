import os
from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from image.models import Image, Gallery
from tier.models import ProfileTier

class ImageTest(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(username='test1', password='1234567')
        self.profile = user.profile


    def test_amt_upload_images_tier_enterprise(self):

        tier = ProfileTier.objects.get(id=3)
        self.profile.profile_tier = tier
        self.profile.save()

        image_path = os.path.join(settings.BASE_DIR, 'static', 'test', 'test.jpeg')
        with open(image_path, 'rb') as image_file:
            img = SimpleUploadedFile('test.jpeg', image_file.read(), content_type='image/jpeg')

        img_obj = Image.objects.create(
            profile=self.profile,
            image=img
        )

        amt_img = Image.objects.filter(profile=self.profile).count()

        # why 4? 1.original img, 2. 200 px img, 3. 400 px img, 4. bin img
        self.assertTrue(amt_img, 4)
        img_org = Image.objects.get(id=1)
        img_200 = Image.objects.get(id=2)
        img_400 = Image.objects.get(id=3)
        img_bin = Image.objects.get(id=4)
        self.assertTrue(
            img_org.image.name.split('/')[-1] == 'test.jpeg',
        )
        self.assertTrue(
            img_200.image.name.split('/')[-1] == '200__test.jpeg',

        )
        self.assertTrue(
            img_400.image.name.split('/')[-1] == '400__test.jpeg',

        )
        self.assertTrue(
            img_bin.image.name.split('/')[-1] == 'binary__test.jpeg',
        )
        # check Gallery:
        img_in_gallery = Gallery.objects.first()
        self.assertEqual(img_in_gallery.images.count(),4)



    def test_images_tier_enterprise_random(self):

        tier = ProfileTier.objects.get(id=3)
        self.profile.profile_tier = tier
        self.profile.save()

        image_path = os.path.join(settings.BASE_DIR, 'static', 'test', 'test.jpeg')
        with open(image_path, 'rb') as image_file:
            img = SimpleUploadedFile('test.jpeg', image_file.read(), content_type='image/jpeg')

        img_obj = Image.objects.create(
            profile=self.profile,
            image=img
        )

        img_bin = Image.objects.last()

        self.assertTrue(img_bin.expiry >= 300 or img_bin.expiry <=30000)
        self.assertFalse(img_bin.is_original)
        self.assertTrue(img_bin.is_active)

    # def test_images_tier_enterprise_expiration(self):
    #     tier = ProfileTier.objects.get(id=3)
    #     self.profile.profile_tier = tier
    #     self.profile.save()
    #
    #     image_path = os.path.join(settings.BASE_DIR, 'static', 'test', 'test.jpeg')
    #     with open(image_path, 'rb') as image_file:
    #         img = SimpleUploadedFile('test.jpeg', image_file.read(), content_type='image/jpeg')
    #
    #     img_obj = Image.objects.create(
    #         profile=self.profile,
    #         image=img,
    #         expiry=300
    #     )
    #     img_obj.created = timezone.now() - timedelta(seconds=305)
    #     img_obj.save()
    #     print(img_obj.created > timezone.now())
    #     print(img_obj.link_active)
    #     print(img_obj.is_active)
    #     sleep(2)
    #     self.assertFalse(img_obj.link_active)

    def test_amt_upload_images_tier_premium(self):

        tier = ProfileTier.objects.get(id=2)
        self.profile.profile_tier = tier
        self.profile.save()

        image_path = os.path.join(settings.BASE_DIR, 'static', 'test', 'test.jpeg')
        with open(image_path, 'rb') as image_file:
            img = SimpleUploadedFile('test.jpeg', image_file.read(), content_type='image/jpeg')

        img_obj = Image.objects.create(
            profile=self.profile,
            image=img
        )

        amt_img = Image.objects.filter(profile=self.profile).count()

        # why 3? 1.original img, 2. 200 px img, 3. 400 px img
        self.assertTrue(amt_img, 3)
        img_org = Image.objects.get(id=1)
        img_200 = Image.objects.get(id=2)
        img_400 = Image.objects.get(id=3)

        self.assertTrue(
            img_org.image.name.split('/')[-1] == 'test.jpeg',
        )
        self.assertTrue(
            img_200.image.name.split('/')[-1] == '200__test.jpeg',

        )
        self.assertTrue(
            img_400.image.name.split('/')[-1] == '400__test.jpeg',

        )

        # check Gallery:
        img_in_gallery = Gallery.objects.first()
        self.assertEqual(img_in_gallery.images.count(),3)

    def test_amt_upload_images_tier_basic(self):

        tier = ProfileTier.objects.get(id=2)
        self.profile.profile_tier = tier
        self.profile.save()

        image_path = os.path.join(settings.BASE_DIR, 'static', 'test', 'test.jpeg')
        with open(image_path, 'rb') as image_file:
            img = SimpleUploadedFile('test.jpeg', image_file.read(), content_type='image/jpeg')

        img_obj = Image.objects.create(
            profile=self.profile,
            image=img
        )

        amt_img = Image.objects.filter(profile=self.profile).count()

        # why 1? only  200 px
        self.assertTrue(amt_img, 1)
        img_200 = Image.objects.get(id=2)


        self.assertTrue(
            img_200.image.name.split('/')[-1] == '200__test.jpeg',

        )


    def tearDown(self) -> None:
        image_path = os.path.join(settings.MEDIA_ROOT, '1')
        for file_name in os.listdir(image_path):
            if file_name.startswith('200__test') or file_name.startswith('400__test') or \
                file_name.startswith('binary__test') or file_name.startswith('test_') or file_name == 'test.jpeg':
                os.remove(os.path.join(image_path, file_name))