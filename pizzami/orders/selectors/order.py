from django.db.models import QuerySet

from pizzami.orders.models import Order
from pizzami.users.models import Profile


def get_orders(user_created: bool, user: Profile = None) -> QuerySet[Order]:
    if user_created:
        return Order.objects.filter(cart__user=user)
    else:
        return Order.objects.all()
