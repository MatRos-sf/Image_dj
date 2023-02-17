from rest_framework import serializers

from image.models import Image, Gallery
from user.models import Profile

class BasicUploadSerializer(serializers.ModelSerializer):

    profile = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Image
        fields = ['profile', 'image', 'id']

    def get_profile(self, obj):
        return self.context['request'].user.profile.pk

    def create(self, validated_data):
        user = self.context['request'].user
        profile = Profile.objects.get(user=user)
        validated_data['profile'] = profile
        return super().create(validated_data)


class ExtendedUploadSerializer(serializers.ModelSerializer):

    profile = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Image
        fields = ['profile', 'image', 'expiry','id']

    def get_profile(self, obj):
        return self.context['request'].user.profile.pk

    def create(self, validated_data):
        user = self.context['request'].user
        profile = Profile.objects.get(user=user)
        validated_data['profile'] = profile
        return super().create(validated_data)

class GallerySerializer(serializers.ModelSerializer):
    images = BasicUploadSerializer(many=True, read_only=True)
    class Meta:
        model = Gallery
        fields = ('id', 'name', 'author', 'images')

