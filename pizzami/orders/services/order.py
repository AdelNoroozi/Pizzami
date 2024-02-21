from rest_framework.utils.serializer_helpers import ReturnDict

from pizzami.orders.selectors import get_or_create_cart
from pizzami.orders.serializers import OrderInputSerializer, OrderDetailedOutputSerializer
from pizzami.users.models import BaseUser


def create_or_update_order(data: dict, user: BaseUser) -> ReturnDict | None:
    cart = get_or_create_cart(user=user.profile)
    if cart.items.count() == 0:
        return None
    serializer = OrderInputSerializer(data=data, context={"cart": cart})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    response_serializer = OrderDetailedOutputSerializer(serializer.instance)
    return response_serializer.data
