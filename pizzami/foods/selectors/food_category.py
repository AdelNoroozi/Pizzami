from django.db.models import QuerySet

from pizzami.foods.models import FoodCategory


def get_food_categories(return_all: bool) -> QuerySet[FoodCategory]:
    if return_all:
        return FoodCategory.objects.all()
    else:
        return FoodCategory.objects.active()


def delete_food_category(food_category: FoodCategory):
    food_category.delete()
