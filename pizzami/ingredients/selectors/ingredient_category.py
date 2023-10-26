from django.db.models import QuerySet

from pizzami.ingredients.models import IngredientCategory


def get_ingredient_categories(return_all: bool) -> QuerySet[IngredientCategory]:
    if return_all:
        return IngredientCategory.objects.all()
    else:
        return IngredientCategory.objects.active()


def delete_ingredient_category(ingredient_category: IngredientCategory) -> None:
    ingredient_category.delete()
