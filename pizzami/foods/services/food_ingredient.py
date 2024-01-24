from pizzami.foods.models import Food
from pizzami.foods.serializers import FoodIngredientInputSerializer


def create_food_ingredient(food: Food, data: dict):
    context = {"food": food}
    serializer = FoodIngredientInputSerializer(data=data, context=context)
    serializer.is_valid(raise_exception=True)
    serializer.save()
