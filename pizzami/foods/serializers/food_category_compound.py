from rest_framework import serializers

from pizzami.foods.models import FoodCategoryCompound
from pizzami.ingredients.serializers import IngredientCategoryBaseOutputSerializer


class FoodCategoryCompoundSerializer(serializers.ModelSerializer):
    ingredient_category = IngredientCategoryBaseOutputSerializer(many=False)

    class Meta:
        model = FoodCategoryCompound
        fields = ("ingredient_category", "min", "max")