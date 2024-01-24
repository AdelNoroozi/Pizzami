from django.db import transaction
from rest_framework import serializers

from pizzami.common.validators import string_included_validator, string_ending_validator
from pizzami.foods.models import FoodCategory
from pizzami.foods.serializers.food_category_compound import FoodCategoryCompoundSerializer, \
    FoodCategoryCompoundInputSerializer


class FoodCategoryBaseOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategory
        fields = ("id", "name", "icon_url", "icon_alt_text")


class FoodCategoryDetailedOutputSerializer(serializers.ModelSerializer):
    compounds = FoodCategoryCompoundSerializer(many=True, read_only=True)

    class Meta:
        model = FoodCategory
        fields = ("id", "image_url", "image_alt_text", "name", "icon_url", "icon_alt_text", "compounds")


class FoodCategoryCompleteOutputSerializer(FoodCategoryDetailedOutputSerializer):
    class Meta(FoodCategoryDetailedOutputSerializer.Meta):
        fields = "__all__"


class FoodCategoryInputSerializer(serializers.ModelSerializer):
    # this field is only for defining structure and is not used for creating or updating compounds.
    compounds = FoodCategoryCompoundInputSerializer(many=True, required=True)

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

    @transaction.atomic
    def save(self, **kwargs):
        self.validated_data.pop("compounds", [])
        return super().save(**kwargs)
