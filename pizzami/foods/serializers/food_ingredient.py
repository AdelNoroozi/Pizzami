from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from pizzami.foods.models import FoodIngredient, FoodCategoryCompound
from pizzami.ingredients.models import Ingredient


class FoodIngredientInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodIngredient
        fields = ("ingredient", "amount")

    def validate(self, data):
        food_category = self.context.get("food_category")
        ingredient = Ingredient.objects.filter(id=data["ingredient"]).first()
        food_category_compounds = FoodCategoryCompound.objects.filter(food_category=food_category,
                                                                      ingredient_category=ingredient.category)
        if food_category_compounds.count() == 0:
            raise ValidationError(_("foods from this category can not have this ingredient"), code="invalid_ingredient")
        food_category_compound = food_category_compounds.first()
        if data["amount"] >= food_category_compound.max or data["amount"] <= food_category_compound.min:
            raise ValidationError(
                _(f"invalid amount of ingredient."
                  f" (min = {food_category_compound.min} - max = {food_category_compound.max})"),
                code="invalid_ingredient_amount")
        return data

    @transaction.atomic
    def create(self, validated_data):
        food = self.context.get("food")
        validated_data["food"] = food
        return super().create(validated_data)


class FoodIngredientOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodIngredient
        exclude = ("active", "food")
