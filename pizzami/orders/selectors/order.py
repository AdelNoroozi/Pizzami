from django.db.models import QuerySet, Q

from pizzami.orders.models import Order
from pizzami.users.models import Profile


def get_orders(user_created: bool, user: Profile = None) -> QuerySet[Order]:
    if user_created:
        return Order.objects.active().filter(cart__user=user)
    else:
        return Order.objects.all()


def search_order(queryset: QuerySet[Order], search_param: str) -> QuerySet[Order]:
    return queryset.filter(
        Q(address__icontains=search_param) |
        Q(cart__items__food__name__icontains=search_param) |
        Q(cart__items__food__category__name__icontains=search_param) |
        Q(cart__user__public_name__icontains=search_param)
    ).distinct()


def order_orders(queryset: QuerySet[Order], order_param: str) -> QuerySet[Order]:
    return queryset.order_by(order_param)
