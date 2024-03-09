from rest_framework import serializers

from pizzami.common.serializers import PaginatedOutputSerializer
from pizzami.common.validators import string_ending_validator, string_included_validator
from pizzami.ingredients.models import IngredientCategory


class IngredientCategoryInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientCategory
        fields = ("name", "image_url", "image_alt_text", "is_active")

    def validate_image_alt_text(self, value):
        string_ending_validator(
            field_name="image alt text",
            str_value=value,
            ending_str="ingredient category"
        )
        string_included_validator(
            field_name="image alt text",
            str_value=value,
            including_str=self.initial_data.get("name"),
            included_helper="category's name"
        )
        return value


class IngredientCategoryBaseOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientCategory
        exclude = ("created_at", "updated_at", "is_active")


class IngredientCategoryCompleteOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientCategory
        fields = "__all__"


class IngredientCategoryPaginatedOutputSerializer(PaginatedOutputSerializer):
    class ResultsOutputSerializer(PaginatedOutputSerializer.ResultsOutputSerializer):
        data = IngredientCategoryCompleteOutputSerializer(many=True)

    results = ResultsOutputSerializer(many=False)
