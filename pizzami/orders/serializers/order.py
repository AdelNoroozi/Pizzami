from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from pizzami.orders.models import Order, Discount
from pizzami.orders.selectors import inquiry_discount_by_id
from pizzami.orders.serializers import CartCompleteOutputsSerializer, DiscountBaseOutputSerializer
from pizzami.users.serializers import ProfileReferenceSerializer


class OrderInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("discount", "address", "has_delivery")

    def validate(self, data):
        if data.get("discount"):
            discount = inquiry_discount_by_id(discount_id=data.get("discount").id, user=self.context.get("cart").user)
            if not discount:
                raise ValidationError(_("invalid discount"))
            else:
                discount_type = discount.type
                self.context["discount_type"] = discount_type
                if discount.type == Discount.TYPE_RATIO:
                    value = discount.percentage_value
                else:
                    value = discount.absolute_value
                self.context["discount_value"] = value

        if data.get("has_delivery") is True and (data.get("address") is None or data.get("address") == ""):
            raise ValidationError(_("orders that have delivery must have an address"))

        return data

    @transaction.atomic
    def save(self, **kwargs):
        validated_data = self.validated_data
        cart = self.context.get("cart")
        discount = self.validated_data.get("discount")
        validated_data["cart"] = cart
        final_value = cart.total_value()
        if discount:
            discount_type = self.context.get("discount_type")
            discount_value = self.context.get("discount_value")
            if discount_type == Discount.TYPE_RATIO:
                final_value = ((100 - discount_value) / 100) * cart.total_value()
            elif discount_type == Discount.TYPE_ABSOLUTE:
                value = cart.total_value() - discount_value
                if value < 0:
                    final_value = 0
                else:
                    final_value = value
        validated_data["final_value"] = final_value
        return super().save(**kwargs)


class OrderBaseOutputSerializer(serializers.ModelSerializer):
    cart__user = ProfileReferenceSerializer(many=False)

    class Meta:
        model = Order
        fields = ("id", "cart__user", "has_delivery", "address", "status", "final_value")


class OrderDetailedOutputSerializer(serializers.ModelSerializer):
    cart = CartCompleteOutputsSerializer(many=False)
    discount = DiscountBaseOutputSerializer(many=False)

    class Meta:
        model = Order
        fields = "__all__"


class UpdateOrderStatusSerializer(serializers.Serializer):
    STATUS_MANUAL_CHOICES = (
        (Order.STATUS_REJECTED, "rejected"),
        (Order.STATUS_IN_PROGRESS, "in progress"),
        (Order.STATUS_DELIVERED, "delivered"),
    )
    status = serializers.ChoiceField(choices=STATUS_MANUAL_CHOICES)

