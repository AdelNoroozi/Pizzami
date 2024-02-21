from rest_framework.utils.serializer_helpers import ReturnDict

from pizzami.orders.serializers import OrderInputSerializer, OrderDetailedOutputSerializer
from pizzami.users.models import BaseUser


def create_or_update_order(data: dict, user: BaseUser) -> ReturnDict:
    serializer = OrderInputSerializer(data=data, context={"user": user.profile})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    response_serializer = OrderDetailedOutputSerializer(serializer.instance)
    return response_serializer.data
