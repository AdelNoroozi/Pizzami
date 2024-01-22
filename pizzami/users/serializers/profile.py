from rest_framework import serializers

from pizzami.users.models import Profile


class ProfileOutputSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email")

    class Meta:
        model = Profile
        fields = ("email", "bio", "public_name")


class ProfileReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("id", "public_name")
