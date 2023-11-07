from pizzami.foods.serializers import FoodCategoryCompoundInputSerializer


def create_food_category_compound(data: dict):
    serializer = FoodCategoryCompoundInputSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
