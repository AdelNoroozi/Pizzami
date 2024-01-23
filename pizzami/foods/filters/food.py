from django_filters import FilterSet

from pizzami.foods.models import Food


class FoodFilter(FilterSet):
    class Meta:
        model = Food
        fields = {
            "category": ["exact"],
            "created_by": ["exact"],
            "is_original": ["exact"],
            "price": ["lt", "gt"],
            "is_confirmed": ["exact"],
            "is_public": ["exact"]
        }
