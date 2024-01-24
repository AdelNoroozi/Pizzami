from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from pizzami.foods.models import FoodCategoryCompound
from pizzami.ingredients.serializers import IngredientCategoryBaseOutputSerializer


class FoodCategoryCompoundSerializer(serializers.ModelSerializer):
    ingredient_category = IngredientCategoryBaseOutputSerializer(many=False)

    class Meta:
        model = FoodCategoryCompound
        fields = ("ingredient_category", "min", "max")


class FoodCategoryCompoundInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodCategoryCompound
        exclude = ("is_active", "id", "position", "food_category")

    def validate(self, data):
        if data["min"] > data["max"]:
            raise ValidationError(_("min value is greater than max value"), code="invalid_min_max_error")
        return data

    @transaction.atomic
    def create(self, validated_data):
        food_category = self.context.get("food_category")
        validated_data["food_category"] = food_category
        return super().create(validated_data)
