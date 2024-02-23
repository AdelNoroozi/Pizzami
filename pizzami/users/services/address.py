import uuid

from rest_framework.generics import get_object_or_404
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList

from pizzami.users.models import BaseUser, Address
from pizzami.users.selectors import get_addresses_by_user, search_address
from pizzami.users.serializers import AddressOutputSerializer, AddressInputSerializer


def get_my_addresses(user: BaseUser, search_param: str = None) -> ReturnList[Address]:
    queryset = get_addresses_by_user(user=user.profile)
    if search_param:
        queryset = search_address(queryset=queryset, search_param=search_param)
    serializer = AddressOutputSerializer(queryset, many=True)
    return serializer.data


def create_address(data: dict, user: BaseUser) -> ReturnDict[Address]:
    serializer = AddressInputSerializer(data=data, context={"user": user.profile})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    response_serializer = AddressOutputSerializer(serializer.instance)
    return response_serializer.data


def update_address(address_id: uuid, data: dict, user: BaseUser) -> ReturnDict[Address]:
    address = get_object_or_404(Address, id=address_id, is_active=True, user=user.profile)
    serializer = AddressInputSerializer(instance=address, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    response_serializer = AddressOutputSerializer(serializer.instance)
    return response_serializer.data
