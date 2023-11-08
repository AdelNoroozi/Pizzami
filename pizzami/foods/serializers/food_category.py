from rest_framework import serializers

from pizzami.common.validators import string_included_validator, string_ending_validator
from pizzami.foods.models import FoodCategory
from pizzami.foods.serializers.food_category_compound import FoodCategoryCompoundSerializer


class FoodCategoryBaseOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = ("id", "name", "icon_url", "icon_alt_text")


class FoodCategoryDetailedOutputSerializer(serializers.ModelSerializer):
    compounds = FoodCategoryCompoundSerializer(many=True)

    class Meta:
        model = FoodCategory
        fields = ("id", "image_url", "image_alt_text", "name", "icon_url", "icon_alt_text", "compounds")


class FoodCategoryCompleteOutputSerializer(FoodCategoryDetailedOutputSerializer):
    class Meta(FoodCategoryDetailedOutputSerializer.Meta):
        fields = "__all__"


class FoodCategoryInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        exclude = ("id", "position", "created_at", "updated_at")

    def validate_image_alt_text(self, value):
        string_ending_validator(
            field_name="image alt text",
            str_value=value,
            ending_str="food category"
        )
        string_included_validator(
            field_name="image alt text",
            str_value=value,
            including_str=self.initial_data.get("name"),
            included_helper="food category's name"
        )
        return value

    def validate_icon_alt_text(self, value):
        string_ending_validator(
            field_name="icon alt text",
            str_value=value,
            ending_str="food category"
        )
        string_included_validator(
            field_name="icon alt text",
            str_value=value,
            including_str=self.initial_data.get("name"),
            included_helper="food category's name"
        )
        return value
