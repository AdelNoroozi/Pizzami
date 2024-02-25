from django.db import transaction
from rest_framework.utils.serializer_helpers import ReturnDict

from pizzami.foods.services import add_food_ordered_count
from pizzami.ingredients.services import update_ingredients_amount_for_cart
from pizzami.orders.models import Payment, Order, CartItem
from pizzami.orders.serializers import PaymentGenericSerializer
from pizzami.orders.services import change_order_status


@transaction.atomic
def create_payment(data: dict) -> ReturnDict[Payment]:
    serializer = PaymentGenericSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    order = serializer.instance.order
    change_order_status(order=order, status=Order.STATUS_PAID)
    cart = order.cart
    cart.is_alive = False
    cart.save()
    update_ingredients_amount_for_cart(cart=cart)
    items = CartItem.objects.filter(cart=cart)
    for item in items:
        add_food_ordered_count(food=item.food, count=item.count)
    return serializer.data

