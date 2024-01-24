from pizzami.foods.models import Food
from pizzami.foods.serializers import FoodIngredientInputSerializer


def create_food_ingredient(food: Food, data: dict):
    context = {"food": food, "food_category": food.category}
    serializer = FoodIngredientInputSerializer(data=data, context=context)
    serializer.is_valid(raise_exception=True)
    serializer.save()
