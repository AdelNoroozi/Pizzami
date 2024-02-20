from rest_framework import serializers

from pizzami.foods.serializers import FoodBaseOutputSerializer
from pizzami.orders.models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    food = FoodBaseOutputSerializer(many=False)

    class Meta:
        model = CartItem
        fields = ("id", "food", "count")
