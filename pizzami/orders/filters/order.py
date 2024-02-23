from django_filters import FilterSet

from pizzami.orders.models import Order


class OrderFilter(FilterSet):
    class Meta:
        model = Order
        fields = {
            "is_active": ["exact"],
            "discount": ["exact"],
            "has_delivery": ["exact"],
            "final_value": ["lt", "gt"],
            "cart__items__food": ["exact"],
            "cart__items__food__category": ["exact"],
            "cart__user": ["exact"]
        }
