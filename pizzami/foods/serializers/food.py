from rest_framework import serializers

from pizzami.foods.models import Food


class FoodBaseOutputSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.icon_url")
    ingredients_str = serializers.SerializerMethodField()

    class Meta:
        model = Food
        fields = ("id", "name", "category", "rate", "ingredients_str")

    def get_ingredients_str(self, obj: Food) -> str:
        ingredients = obj.ingredients
        ingredients_flat = ""
        for ingredient in ingredients:
            ingredients_flat += ingredient.amount + ingredient.ingredient.unit + ingredient.ingredient.name + ", "
        return ingredients_flat
