from django.db import transaction
from rest_framework.generics import get_object_or_404

from pizzami.foods.models import Food
from pizzami.orders.selectors import get_or_create_cart, get_or_create_cart_item, delete_cart_item
from pizzami.users.models import BaseUser


@transaction.atomic
def add_to_cart(food_id: str, count: int, user: BaseUser):
    cart = get_or_create_cart(user=user.profile)
    food = get_object_or_404(Food, id=food_id)
    cart_item = get_or_create_cart_item(cart=cart, food=food)
    count_sum = cart_item.count + count
    if count_sum <= 0:
        delete_cart_item(cart_item=cart_item)
    else:
        cart_item.count = count_sum
        cart_item.save()
