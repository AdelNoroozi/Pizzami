from rest_framework import serializers

from pizzami.foods.models import Food, FoodIngredient


class FoodBaseOutputSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.icon_url")
    ingredients_str = serializers.SerializerMethodField()

    class Meta:
        model = Food
        fields = ("id", "name", "price", "category", "rate", "ingredients_str")

    def get_ingredients_str(self, obj: Food) -> str:
        ingredients = FoodIngredient.objects.filter(food=obj).values_list(
            'amount', 'ingredient__unit', 'ingredient__name'
        )
        ingredients_flat = [
            f"{amount} {unit} of {name}" for amount, unit, name in ingredients
        ]
        return ", ".join(ingredients_flat) if ingredients_flat else "No ingredients"

