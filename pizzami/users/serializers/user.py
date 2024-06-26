from django.contrib.auth import authenticate
from django.core.validators import MinLengthValidator
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from pizzami.common.serializers import PaginatedOutputSerializer
from pizzami.users.models import BaseUser, Profile
from pizzami.users.validators import number_validator, letter_validator, special_char_validator


class RegisterInputSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    bio = serializers.CharField(max_length=1000, required=False)
    public_name = serializers.CharField(max_length=50, required=True)
    password = serializers.CharField(
        validators=[
            number_validator,
            letter_validator,
            special_char_validator,
            MinLengthValidator(limit_value=10)
        ]
    )
    confirm_password = serializers.CharField(max_length=255)

    def validate_email(self, email):
        if BaseUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("email Already Taken")
        return email

    def validate_public_name(self, public_name):
        if Profile.objects.filter(public_name=public_name).exists():
            raise serializers.ValidationError("public_name Already Taken")
        return public_name

    def validate(self, data):
        if not data.get("password") or not data.get("confirm_password"):
            raise serializers.ValidationError("Please fill password and confirm password")

        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError("confirm password is not equal to password")
        return data


class AdminInputSerializer(RegisterInputSerializer):
    bio = None
    public_name = None


class RegisterOutputSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField("get_token")

    class Meta:
        model = BaseUser
        fields = ("email", "token", "created_at", "updated_at")

    def get_token(self, user):
        data = dict()
        token_class = RefreshToken

        refresh = token_class.for_user(user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data


class UserOutputSerializer(serializers.ModelSerializer):
    public_name = serializers.SerializerMethodField()
    bio = serializers.SerializerMethodField()

    class Meta:
        model = BaseUser
        exclude = ("password", "groups", "user_permissions")

    def get_public_name(self, obj: BaseUser):
        if hasattr(obj, "profile"):
            return obj.profile.public_name

    def get_bio(self, obj: BaseUser):
        if hasattr(obj, "profile"):
            return obj.profile.bio


class UserPaginatedOutputSerializer(PaginatedOutputSerializer):
    class UserResultsOutputSerializer(PaginatedOutputSerializer.ResultsOutputSerializer):
        data = UserOutputSerializer(many=True)

    results = UserResultsOutputSerializer(many=False)


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    def validate(self, data):
        email = data.get("email")
        if not BaseUser.objects.filter(is_active=True, email=email).exists():
            raise serializers.ValidationError("no active user found with this email")

        return data


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        validators=[
            number_validator,
            letter_validator,
            special_char_validator,
            MinLengthValidator(limit_value=10)
        ]
    )
    confirm_password = serializers.CharField(max_length=255)

    def validate(self, data):
        if not data.get("password") or not data.get("confirm_password"):
            raise serializers.ValidationError("Please fill password and confirm password")

        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError("confirm password is not equal to password")
        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=255)
    password = serializers.CharField(
        validators=[
            number_validator,
            letter_validator,
            special_char_validator,
            MinLengthValidator(limit_value=10)
        ]
    )
    confirm_password = serializers.CharField(max_length=255)

    def validate_old_password(self, value):
        if not authenticate(email=self.context.get("user").email, password=value):
            raise serializers.ValidationError("old password is incorrect")

        return value

    def validate(self, data):
        if not data.get("password") or not data.get("confirm_password"):
            raise serializers.ValidationError("Please fill password and confirm password")

        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError("confirm password is not equal to password")

        if data.get("password") == data.get("old_password"):
            raise serializers.ValidationError("old password and new password can't be the same")

        return data
