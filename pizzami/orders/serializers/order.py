from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from pizzami.common.serializers import PaginatedOutputSerializer
from pizzami.orders.models import Order, Discount
from pizzami.orders.selectors import inquiry_discount_by_id
from pizzami.orders.serializers import CartCompleteOutputsSerializer, DiscountBaseOutputSerializer
from pizzami.orders.serializers.payment import PaymentReferenceOutput
from pizzami.users.serializers import ProfileReferenceSerializer


class OrderInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("discount", "address", "has_delivery")

    def validate_address(self, value):
        if value and value.user != self.context.get("cart").user:
            raise ValidationError(_(f"Invalid pk \"{value.id}\" - object does not exist."))

    def validate_discount(self, value):
        if value:
            discount = inquiry_discount_by_id(discount_id=value.id, user=self.context.get("cart").user)
            if not discount:
                raise ValidationError(_(f"Invalid pk \"{value.id}\" - object does not exist."))
            else:
                discount_type = discount.type
                self.context["discount_type"] = discount_type
                if discount.type == Discount.TYPE_RATIO:
                    discount_value = discount.percentage_value
                else:
                    discount_value = discount.absolute_value
                self.context["discount_value"] = discount_value

    def validate(self, data):
        address = data.get("address")
        if data.get("has_delivery") is True and (address is None or address == ""):
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
        address = self.validated_data.get("address")
        if address:
            validated_data["address_str"] = address.address_str + " / " + str(address.phone_number)
        return super().save(**kwargs)


class OrderBaseOutputSerializer(serializers.ModelSerializer):
    cart_user = serializers.SerializerMethodField()
    payments = PaymentReferenceOutput(many=True)

    class Meta:
        model = Order
        fields = ("id", "cart_user", "has_delivery", "address", "status", "final_value", "payments")

    def get_cart_user(self, obj):
        return ProfileReferenceSerializer(obj.cart.user).data


class OrderDetailedOutputSerializer(serializers.ModelSerializer):
    cart = CartCompleteOutputsSerializer(many=False)
    discount = DiscountBaseOutputSerializer(many=False)
    payments = PaymentReferenceOutput(many=True)

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


class OrderPaginatedOutputSerializer(PaginatedOutputSerializer):
    class OrderResultsOutputSerializer(PaginatedOutputSerializer.ResultsOutputSerializer):
        data = OrderBaseOutputSerializer(many=True)

    results = OrderResultsOutputSerializer(many=False)
