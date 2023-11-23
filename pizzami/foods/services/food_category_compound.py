import uuid

from pizzami.foods.models import FoodCategory
from pizzami.foods.serializers import FoodCategoryCompoundInputSerializer


def create_food_category_compound(food_category: FoodCategory, data: dict):
    context = {"food_category": food_category}
    serializer = FoodCategoryCompoundInputSerializer(data=data, context=context)
    serializer.is_valid(raise_exception=True)
    serializer.save()
