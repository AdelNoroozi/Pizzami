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


class ProfileUpdateSerializer(serializers.Serializer):
    bio = serializers.CharField(max_length=1000, required=False)
    public_name = serializers.CharField(max_length=1000, required=False)
    custom_fields = serializers.JSONField(required=False)
