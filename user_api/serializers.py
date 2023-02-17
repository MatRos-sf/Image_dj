from rest_framework import serializers

from user.models import Profile

class ProfileSerializers(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['user', 'profile_tier']
