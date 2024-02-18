from django_filters import FilterSet

from pizzami.orders.models import Discount


class DiscountFilter(FilterSet):
    class Meta:
        model = Discount
        fields = {
            "is_active": ["exact"],
            "is_public": ["exact"],
            "has_time_limit": ["exact"],
            "type": ["exact"],
            "specified_to_type": ["exact"]
        }
