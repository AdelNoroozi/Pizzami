from pizzami.foods.models import FoodCategory, FoodCategoryCompound


def delete_compounds_by_food_category(food_category: FoodCategory):
    FoodCategoryCompound.objects.filter(food_category=food_category).delete()
