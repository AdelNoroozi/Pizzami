from django.db import transaction
from rest_framework.utils.serializer_helpers import ReturnDict

from pizzami.users.models import BaseUser
from pizzami.users.selectors.profile import create_profile
from pizzami.users.serializers import RegisterInputSerializer, RegisterOutputSerializer
from pizzami.users.services import send_welcome_mail


def create_user(email: str, password: str) -> BaseUser:
    return BaseUser.objects.create_user(email=email, password=password)

@transaction.atomic
def register(data: dict) -> ReturnDict:
    serializer = RegisterInputSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    if "bio" in data:
        bio = data.pop("bio")
    else:
        bio = ""
    public_name = data.pop("public_name")
    data.pop("confirm_password")
    user = create_user(email=data.get("email"), password=data.get("password"))

    create_profile(user=user, bio=bio, public_name=public_name)

    send_welcome_mail(user=user, public_name=public_name)

    return RegisterOutputSerializer(user).data


@transaction.atomic
def create_admin(data: dict):
    serializer = RegisterInputSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    BaseUser.objects.create_admin(email=data.get("email"), password=data.get("password"))
