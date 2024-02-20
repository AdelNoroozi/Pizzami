from rest_framework import serializers

from pizzami.orders.models import Cart
from pizzami.orders.serializers import CartItemSerializer


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ("id", "created_at", "items")
