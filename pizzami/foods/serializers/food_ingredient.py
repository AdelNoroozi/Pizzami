from django.db import transaction
from django.db.models import Sum, F
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from pizzami.foods.models import FoodIngredient, FoodCategoryCompound
from pizzami.ingredients.models import Ingredient


class FoodIngredientBaseInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = FoodIngredient
        fields = ("ingredient", "amount")


class FoodIngredientInputSerializer(FoodIngredientBaseInputSerializer):

    def validate(self, data):
        food_category = self.context.get("food_category")
        ingredient = Ingredient.objects.filter(id=data["ingredient"].id).first()
        food_category_compounds = FoodCategoryCompound.objects.filter(food_category=food_category,
                                                                      ingredient_category=ingredient.category)
        if food_category_compounds.count() == 0:
            raise ValidationError(_("foods from this category can not have this ingredient"), code="invalid_ingredient")
        food_category_compound = food_category_compounds.first()
        # must be refactored
        previous_amounts = FoodIngredient.objects.filter(
            food=self.context.get("food"), ingredient__category=ingredient.category).aggregate(
            amount_sum=Sum(F("amount")))["amount_sum"]
        total_amount = data["amount"] if previous_amounts is None else data["amount"] + previous_amounts
        if total_amount > food_category_compound.max or total_amount < food_category_compound.min:
            raise ValidationError(
                _(f"invalid amount of {ingredient.category.name}."
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
        exclude = ("food", )
