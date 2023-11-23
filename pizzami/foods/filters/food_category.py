from django_filters import FilterSet

from pizzami.foods.models import FoodCategory


class FoodCategoryFilter(FilterSet):
    class Meta:
        model = FoodCategory
        fields = {
            "is_customizable": ["exact"]
        }
