from django.db import transaction
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList

from pizzami.users.filters import UserFilter
from pizzami.users.models import BaseUser
from pizzami.users.selectors import get_users as get_users_selector, search_users
from pizzami.users.selectors.profile import create_profile
from pizzami.users.serializers import RegisterInputSerializer, RegisterOutputSerializer, AdminInputSerializer, \
    UserOutputSerializer
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
    serializer = AdminInputSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    BaseUser.objects.create_admin(email=data.get("email"), password=data.get("password"))


def get_users(query_dict: dict, is_superuser: bool) -> ReturnList:
    queryset = get_users_selector(base_only=not is_superuser)
    search_param = query_dict.get("search")
    if search_param:
        queryset = search_users(queryset=queryset, search_param=search_param)
    queryset = UserFilter(query_dict, queryset=queryset).qs
    serializer = UserOutputSerializer(queryset, many=True)
    return serializer.data
