from rest_framework import serializers

from pizzami.users.models import Profile


class ProfileBaseOutputSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email")

    class Meta:
        model = Profile
        fields = ("email", "bio", "public_name")


class ProfileFullOutputSerializer(ProfileBaseOutputSerializer):
    def to_representation(self, instance):
        from pizzami.users.services.profile import profile_collection
        data = super().to_representation(instance)
        custom_fields_document = dict(profile_collection.find_one({"core_profile_id": instance.user.profile.id}))
        custom_fields_document.pop("_id", None)
        custom_fields_document.pop("core_profile_id", None)
        data.update(custom_fields_document)
        return data


class ProfilePageOutputSerializer(ProfileFullOutputSerializer):
    email = None

    class Meta:
        model = Profile
        fields = ("public_name", "bio")


class ProfileReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("id", "public_name", "bio")


class ProfileUpdateSerializer(serializers.Serializer):
    bio = serializers.CharField(max_length=1000, required=False)
    public_name = serializers.CharField(max_length=1000, required=False)
    custom_fields = serializers.DictField(required=False)
