from rest_framework import serializers

from pizzami.users.models import Profile


class ProfileOutputSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email")

    class Meta:
        model = Profile
        fields = ("email", "bio")
