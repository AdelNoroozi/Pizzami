from rest_framework import serializers

from pizzami.ingredients.models import Ingredient
from pizzami.ingredients.serializers import IngredientCategoryBaseOutputSerializer


class IngredientBaseOutputSerializer(serializers.ModelSerializer):
    category = IngredientCategoryBaseOutputSerializer(many=False)

    class Meta:
        model = Ingredient
        exclude = ("created_at", "updated_at", "is_active")


class IngredientCompleteOutputSerializer(IngredientBaseOutputSerializer):
    class Meta(IngredientBaseOutputSerializer.Meta):
        exclude = None
        fields = "__all__"
