from rest_framework import serializers

from pizzami.common.serializers import PaginatedOutputSerializer
from pizzami.common.validators import string_included_validator
from pizzami.ingredients.models import Ingredient
from pizzami.ingredients.serializers import IngredientCategoryBaseOutputSerializer


class IngredientInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        exclude = ("id", "created_at", "updated_at", "position")

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


class IngredientPaginatedOutputSerializer(PaginatedOutputSerializer):
    class IngredientResultsOutputSerializer(PaginatedOutputSerializer.ResultsOutputSerializer):
        data = IngredientCompleteOutputSerializer(many=True)

    results = IngredientResultsOutputSerializer(many=False)
