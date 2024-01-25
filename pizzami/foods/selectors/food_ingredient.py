from pizzami.foods.models import Food, FoodIngredient


def delete_food_ingredients_by_food(food: Food):
    FoodIngredient.objects.filter(food=food).delete()
