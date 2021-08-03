from rest_framework import serializers

from myuser.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ['password']

class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ['password']