from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import transaction
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode
from rest_framework.generics import get_object_or_404
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList

from pizzami.users.filters import UserFilter
from pizzami.users.models import BaseUser
from pizzami.users.selectors import get_users as get_users_selector, search_users, order_users
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
    order_param = query_dict.get("order_by")
    if search_param:
        queryset = search_users(queryset=queryset, search_param=search_param)
    if order_param and \
            order_param.lstrip("-") in ["position", "created_at", "updated_at"]:
        queryset = order_users(queryset=queryset, order_param=order_param)
    queryset = UserFilter(query_dict, queryset=queryset).qs
    serializer = UserOutputSerializer(queryset)
    return serializer.data


def change_password(user: BaseUser, password: str):
    user.set_password(password)
    user.save()


def reset_password(uid: str, token: str, password: str) -> bool:
    try:
        _id = smart_str(urlsafe_base64_decode(uid))
        user = get_object_or_404(BaseUser, is_active=True, id=_id)
        if not PasswordResetTokenGenerator().check_token(user=user, token=token):
            return False
        change_password(user=user, password=password)
    except:
        return False
    return True
