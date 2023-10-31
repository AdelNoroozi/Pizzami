from rest_framework import serializers

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


