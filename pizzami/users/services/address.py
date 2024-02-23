from rest_framework.utils.serializer_helpers import ReturnDict

from pizzami.users.models import BaseUser
from pizzami.users.selectors import get_addresses_by_user
from pizzami.users.serializers import AddressOutputSerializer


def get_my_addresses(user: BaseUser, search_param: str = None) -> ReturnDict:
    addresses = get_addresses_by_user(user=user.profile)
    serializer = AddressOutputSerializer(addresses, many=True)
    return serializer.data
