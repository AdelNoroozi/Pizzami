from pizzami.foods.models import Food
from pizzami.orders.models import Cart, CartItem
from pizzami.users.models import Profile


def get_or_create_cart(user: Profile) -> Cart:
    cart = Cart.objects.get_or_create(user=user, is_alive=True)
    return cart


def get_or_create_cart_item(cart: Cart, food: Food) -> CartItem:
    if CartItem.objects.filter(food=food, cart=cart).exists():
        return CartItem.objects.filter(food=food, cart=cart).first()
    return CartItem(food=food, cart=cart, count=0)
