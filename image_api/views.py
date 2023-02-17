from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions

from image.models import Image, Gallery
from .serializers import BasicUploadSerializer, ExtendedUploadSerializer, GallerySerializer

class IsAuthorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
           return False
        return obj.profile == request.user.profile or request.user.is_superuser


class ImageViewSet(ModelViewSet):

    permission_classes = [IsAuthorOrAdmin]
    serializer_class = BasicUploadSerializer

    def get_queryset(self):
        return [ i for i in Image.objects.all() if i.link_active ]

    def get_serializer_class(self):
        user_profile = self.request.user.profile.profile_tier.binary_file

        if user_profile:
            return ExtendedUploadSerializer

        return self.serializer_class


class GalleryViewSet(ModelViewSet):

    permission_classes = [IsAuthorOrAdmin]
    serializer_class = GallerySerializer
    queryset = Gallery.objects.all()




