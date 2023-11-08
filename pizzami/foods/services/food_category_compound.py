import uuid

from pizzami.foods.serializers import FoodCategoryCompoundInputSerializer


def create_food_category_compound(food_category_id: uuid, data: dict):
    data["food_category"] = food_category_id
    serializer = FoodCategoryCompoundInputSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
