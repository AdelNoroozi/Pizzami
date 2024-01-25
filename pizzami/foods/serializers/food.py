from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from pizzami.common.validators import string_included_validator
from pizzami.foods.models import Food, FoodIngredient
from pizzami.foods.serializers.food_ingredient import FoodIngredientOutputSerializer, \
    FoodIngredientBaseInputSerializer
from pizzami.ingredients.models import Ingredient
from pizzami.users.models import Profile
from pizzami.users.serializers import ProfileReferenceSerializer


class FoodBaseOutputSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.icon_url")
    created_by = serializers.CharField(source="created_by.public_name", allow_null=True)
    ingredients_str = serializers.SerializerMethodField()

    class Meta:
        model = Food
        fields = (
            "id", "name", "price", "category", "created_by", "rate", "ordered_count", "is_original", "ingredients_str",
            "image_url", "image_alt_text")

    def get_ingredients_str(self, obj: Food) -> str:
        ingredients = FoodIngredient.objects.filter(food=obj).values_list(
            'amount', 'ingredient__unit', 'ingredient__name'
        )
        ingredients_flat = ""
        for amount, unit, name in ingredients:
            plural_sign = "s" if amount != 1 else ""
            ingredients_flat += f"{amount} {unit}{plural_sign} of {name}, "

        return ingredients_flat.rstrip(", ")


class FoodDetailedOutputSerializer(FoodBaseOutputSerializer):
    created_by = ProfileReferenceSerializer(many=False)

    class Meta(FoodBaseOutputSerializer.Meta):
        fields = None
        exclude = ("description",)


class FoodPublicDetailedOutputSerializer(FoodBaseOutputSerializer):
    ingredients = FoodIngredientOutputSerializer(many=True)
    ingredients_str = None

    class Meta(FoodBaseOutputSerializer.Meta):
        fields = (
            "id", "name", "price", "category", "created_by", "views", "rate", "ordered_count", "is_original",
            "ingredients", "image_url", "image_alt_text", "description")


class FoodCompleteOutputSerializer(FoodDetailedOutputSerializer):
    ingredients = FoodIngredientOutputSerializer(many=True)

    class Meta(FoodDetailedOutputSerializer.Meta):
        exclude = None
        fields = "__all__"


class FoodInputSerializer(serializers.ModelSerializer):
    ingredients = FoodIngredientBaseInputSerializer(many=True, required=False)
    price = serializers.FloatField(required=False)

    class Meta:
        model = Food
        fields = ("name", "category", "description", "ingredients", "image_url", "image_alt_text", "is_public", "price")

    def validate_category(self, value):
        if not value.is_active:
            raise ValidationError(_("category is not active"),
                                  code="deactivated_category")
        return value

    def validate_image_alt_text(self, value):
        string_included_validator(
            field_name="image alt text",
            str_value=value,
            including_str=self.initial_data.get("name"),
            included_helper="food's name"
        )
        return value

    def validate(self, data):
        if self.context.get("user").is_staff and "price" not in data:
            raise ValidationError(_("the price for foods that are created by staff users need to be specified"),
                                  code="price_needed")
        return data

    @staticmethod
    def calculate_price(ingredients):
        total_price = 0
        for ingredient in ingredients:
            price = Ingredient.objects.filter(id=ingredient.get("ingredient").id).first().price
            total_price += price * ingredient.get("amount")
        return total_price * 1.2

    @transaction.atomic
    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients", [])
        current_user = self.context.get("user")
        if not current_user.is_staff:
            profile = Profile.objects.filter(user=current_user).first()
            validated_data["is_original"] = False
            validated_data["created_by"] = profile
            price = self.calculate_price(ingredients=ingredients)
            validated_data["price"] = price
        else:
            validated_data["is_confirmed"] = True
            validated_data["is_public"] = True
        return super().create(validated_data)


class FoodMinorInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ("name", "description", "public")
