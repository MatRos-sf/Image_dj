from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions

from image.models import Image, Gallery
from .serializers import BasicUploadSerializer, ExtendedUploadSerializer, GallerySerializer


class ImageViewSet(ModelViewSet):

    permission_classes = [permissions.IsAdminUser]
    serializer_class = BasicUploadSerializer

    def get_queryset(self):
        return [ i for i in Image.objects.all() if i.link_active ]

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            user_profile = self.request.user.profile.profile_tier.binary_file

            if user_profile:
                return ExtendedUploadSerializer

        return self.serializer_class


class GalleryViewSet(ModelViewSet):

    permission_classes = [permissions.IsAdminUser]
    serializer_class = GallerySerializer
    queryset = Gallery.objects.all()




