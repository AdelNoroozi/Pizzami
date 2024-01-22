from rest_framework import serializers

from pizzami.foods.models import Food, FoodIngredient
from pizzami.users.serializers import ProfileReferenceSerializer


class FoodBaseOutputSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.icon_url")
    created_by = serializers.CharField(source="created_by.public_name")
    ingredients_str = serializers.SerializerMethodField()

    class Meta:
        model = Food
        fields = ("id", "name", "price", "category", "created_by", "rate", "ingredients_str")

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
