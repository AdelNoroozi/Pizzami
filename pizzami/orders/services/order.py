from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework.generics import get_object_or_404
from rest_framework.utils.serializer_helpers import ReturnDict

from pizzami.orders.models import Order
from pizzami.orders.selectors import get_or_create_cart
from pizzami.orders.serializers import OrderInputSerializer, OrderDetailedOutputSerializer
from pizzami.users.models import BaseUser


def create_or_update_order(data: dict, user: BaseUser) -> ReturnDict[Order] | None:
    cart = get_or_create_cart(user=user.profile)
    if cart.items.count() == 0:
        return None
    orders = Order.objects.filter(cart=cart)
    if orders.exists:
        serializer = OrderInputSerializer(instance=orders.first(), data=data, partial=True, context={"cart": cart})
    else:
        serializer = OrderInputSerializer(data=data, context={"cart": cart})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    response_serializer = OrderDetailedOutputSerializer(serializer.instance)
    return response_serializer.data


@transaction.atomic
def submit_my_order(user: BaseUser) -> (bool, str):
    order = get_object_or_404(Order, user=user.profile, status=Order.STATUS_CREATED)
    if order.has_delivery is None:
        return False, _("must determine whether the order has delivery or not.")
    order.status = Order.STATUS_READY_TO_PAY
    order.save()
    return True, _("done")
