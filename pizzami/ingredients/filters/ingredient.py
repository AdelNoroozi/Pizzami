from django_filters import FilterSet

from pizzami.ingredients.models import Ingredient


class IngredientFilter(FilterSet):
    class Meta:
        model = Ingredient
        fields = {
            "category": ["exact"]
        }
