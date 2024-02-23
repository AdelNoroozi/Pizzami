from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList

from pizzami.users.models import BaseUser, Address
from pizzami.users.selectors import get_addresses_by_user
from pizzami.users.serializers import AddressOutputSerializer, AddressInputSerializer


def get_my_addresses(user: BaseUser, search_param: str = None) -> ReturnList[Address]:
    addresses = get_addresses_by_user(user=user.profile)
    serializer = AddressOutputSerializer(addresses, many=True)
    return serializer.data


def create_address(data: dict, user: BaseUser) -> ReturnDict[Address]:
    serializer = AddressInputSerializer(data=data, context={"user": user.profile})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    serializer = AddressOutputSerializer(serializer.instance)
    return serializer.data
