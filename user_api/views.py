from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from user.models import Profile
from .serializers import ProfileSerializers

class ProfileViewSet(ModelViewSet):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializers

