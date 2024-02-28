from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from pizzami.orders.models import Payment, Order


class PaymentGenericSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("order", "tracking_code", "payment_data")

    def validate_order(self, value):
        if value.status != Order.STATUS_READY_TO_PAY:
            raise ValidationError(_("invalid order"))

        return value


class PaymentReferenceOutput(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("id", "tracking_code", "payment_data")
