from rest_framework import serializers

from pizzami.common.validators import string_ending_validator, string_included_validator
from pizzami.ingredients.models import Ingredient
from pizzami.ingredients.serializers import IngredientCategoryBaseOutputSerializer


class IngredientInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        exclude = ("id", "created_at", "updated_at")

    def validate_image_alt_text(self, value):
        string_included_validator(
            field_name="image alt text",
            str_value=value,
            including_str=self.initial_data.get("name"),
            included_helper="ingredient's name"
        )
        return value


class IngredientBaseOutputSerializer(serializers.ModelSerializer):
    category = IngredientCategoryBaseOutputSerializer(many=False)

    class Meta:
        model = Ingredient
        exclude = ("created_at", "updated_at", "is_active")


class IngredientCompleteOutputSerializer(IngredientBaseOutputSerializer):
    class Meta(IngredientBaseOutputSerializer.Meta):
        exclude = None
        fields = "__all__"
