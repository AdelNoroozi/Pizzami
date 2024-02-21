from rest_framework import serializers

from pizzami.orders.models import Cart
from pizzami.orders.serializers import CartItemSerializer
from pizzami.users.serializers import ProfileReferenceSerializer


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ("id", "created_at", "items", "total_value")


class CartCompleteOutputsSerializer(CartSerializer):
    user = ProfileReferenceSerializer(many=False)

    class Meta(CartSerializer.Meta):
        fields = "__all__"
