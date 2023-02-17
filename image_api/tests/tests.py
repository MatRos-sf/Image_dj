import os

from django.shortcuts import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

from rest_framework.test import APITestCase, APIClient

from image.models import Image
from tier.models import ProfileTier

class ImageViewSetTestCase(APITestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpass')
        # self.user.is_staff = True
        # self.user.save()
        self.profile = self.user.profile

    def test_post_tier_basic(self):
        client = APIClient()
        client.force_login(user=self.user)
        # Create an image for the user
        image_path = os.path.join(settings.BASE_DIR, 'static', 'test', 'test.jpeg')
        with open(image_path, 'rb') as image_file:
            img = SimpleUploadedFile('test.jpeg', image_file.read(), content_type='image/jpeg')
        payload = {
            'image': img,
        }
        response = client.post(reverse('api_ownimages-list'), payload)

        self.assertEqual(Image.objects.count(), 1)
        self.assertEqual(response.status_code, 201)

    def test_post_tier_premium(self):

        self.profile.profile_tier = ProfileTier.objects.get(id=2)
        self.profile.save()
        client = APIClient()
        client.force_login(user=self.user)
        # Create an image for the user
        image_path = os.path.join(settings.BASE_DIR, 'static', 'test', 'test.jpeg')
        with open(image_path, 'rb') as image_file:
            img = SimpleUploadedFile('test.jpeg', image_file.read(), content_type='image/jpeg')
        payload = {
            'image': img,
        }
        response = client.post(reverse('api_ownimages-list'), payload)

        self.assertEqual(Image.objects.count(), 3)
        self.assertEqual(response.status_code, 201)

    def test_post_tier_enterprise(self):
        self.profile.profile_tier = ProfileTier.objects.get(id=3)
        self.profile.save()
        client = APIClient()
        client.force_login(user=self.user)
        # Create an image for the user
        image_path = os.path.join(settings.BASE_DIR, 'static', 'test', 'test.jpeg')
        with open(image_path, 'rb') as image_file:
            img = SimpleUploadedFile('test.jpeg', image_file.read(), content_type='image/jpeg')
        payload = {
            'image': img,
            'expiry': 399
        }
        response = client.post(reverse('api_ownimages-list'), payload)

        self.assertEqual(Image.objects.count(), 4)
        self.assertEqual(response.status_code, 201)

    def tearDown(self) -> None:
        image_path = os.path.join(settings.MEDIA_ROOT, '1')
        for file_name in os.listdir(image_path):
            if file_name.startswith('200__test') or file_name.startswith('400__test') or \
                file_name.startswith('binary__test') or file_name.startswith('test_') or file_name == 'test.jpeg':
                os.remove(os.path.join(image_path, file_name))

