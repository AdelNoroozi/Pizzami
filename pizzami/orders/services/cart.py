from django.db import transaction
from django.http import Http404
from rest_framework.generics import get_object_or_404

from pizzami.foods.models import Food
from pizzami.orders.models import Cart, Order
from pizzami.orders.selectors import get_or_create_cart, get_or_create_cart_item, delete_cart_item
from pizzami.users.models import BaseUser


@transaction.atomic
def add_to_cart(food_id: str, count: int, user: BaseUser) -> (Cart | None, bool):
    profile = user.profile
    cart = get_or_create_cart(user=profile)
    if Order.objects.filter(cart=cart).exists():
        from pizzami.orders.services import change_order_status
        change_order_status(order=cart.order, status=Order.STATUS_CREATED)
    food = get_object_or_404(Food, id=food_id, is_active=True)
    if (not food.is_public) and (food.created_by != profile):
        raise Http404
    if not food.is_available:
        return None, "food is not available"
    cart_item = get_or_create_cart_item(cart=cart, food=food)
    count_sum = cart_item.count + int(count)
    if count_sum <= 0:
        delete_cart_item(cart_item=cart_item)
    if count_sum >= 8:
        return None, "can't have more than 7 foods of the same type in 1 order"
    else:
        cart_item.count = count_sum
        cart_item.save()
    return cart, ""
