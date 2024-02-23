import uuid

from django.db import transaction
from django.http import QueryDict
from django.utils.translation import gettext_lazy as _
from rest_framework.generics import get_object_or_404
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList

from pizzami.orders.filters import OrderFilter
from pizzami.orders.models import Order
from pizzami.orders.selectors import get_or_create_cart, create_payment, get_orders as get_orders_selector, \
    search_order, order_orders
from pizzami.orders.serializers import OrderInputSerializer, OrderDetailedOutputSerializer, OrderBaseOutputSerializer
from pizzami.users.models import BaseUser


def change_order_status(order: Order, status: str):
    order.status = status
    order.save()


@transaction.atomic
def create_or_update_order(data: dict, user: BaseUser) -> ReturnDict[Order] | None:
    cart = get_or_create_cart(user=user.profile)
    if cart.items.count() == 0:
        return None
    orders = Order.objects.filter(cart=cart)
    if orders.exists():
        order = orders.first()
        change_order_status(order=order, status=Order.STATUS_CREATED)
        serializer = OrderInputSerializer(instance=order, data=data, partial=True, context={"cart": cart})
    else:
        serializer = OrderInputSerializer(data=data, context={"cart": cart})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    response_serializer = OrderDetailedOutputSerializer(serializer.instance)
    return response_serializer.data


@transaction.atomic
def submit_my_order(user: BaseUser) -> (bool, str):
    order = get_object_or_404(Order, cart__user=user.profile, status=Order.STATUS_CREATED)
    if order.has_delivery is None:
        return False, _("must determine whether the order has delivery or not.")
    change_order_status(order=order, status=Order.STATUS_READY_TO_PAY)
    return True, _("done")


@transaction.atomic
def update_order_status(order_id: uuid, status: str) -> (bool, str):
    order = get_object_or_404(Order, id=order_id)
    current_status = order.status
    if current_status in [Order.STATUS_CREATED, Order.STATUS_READY_TO_PAY]:
        return False, _("order is not paid yet.")
    if current_status in [Order.STATUS_REJECTED, Order.STATUS_DELIVERED]:
        return False, _("can't change status of delivered or rejected orders")
    if current_status == status:
        return False, _(f"order is already in {status} status")
    if status == Order.STATUS_REJECTED:
        payment_data = {
            "order": order,
            "is_income": False,
            # mock data for now
            "tracking_code": "abcdefghijklmnopqrstuvwxyz",
            "payment_data": "zyxwvutseqponmlkjihgfedcba"
        }
        create_payment(data=payment_data)
    change_order_status(order=order, status=status)
    return True, _(f"order status changed to {status}")


def get_orders(query_dict: QueryDict, user_created: bool, user: BaseUser = None) -> ReturnList[Order]:
    if user_created:
        queryset = get_orders_selector(user_created=True, user=user.profile)
    else:
        queryset = get_orders_selector(user_created=False)
    search_param = query_dict.get("search")
    order_param = query_dict.get("order_by")
    if search_param:
        queryset = search_order(queryset=queryset, search_param=search_param)
    queryset = OrderFilter(query_dict, queryset=queryset).qs
    if order_param and order_param.lstrip("-") in ["final_value", "position", "created_at", "modified_at"]:
        queryset = order_orders(queryset=queryset, order_param=order_param)
    serializer = OrderBaseOutputSerializer(queryset, many=True)
    return serializer.data
