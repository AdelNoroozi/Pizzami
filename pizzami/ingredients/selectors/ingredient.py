from django.db.models import QuerySet

from pizzami.ingredients.models import Ingredient


def get_ingredients(return_all: bool) -> QuerySet[Ingredient]:
    if return_all:
        return Ingredient.objects.all()
    else:
        return Ingredient.objects.active()
