from rest_framework import serializers

from pizzami.orders.models import Payment


class PaymentGenericSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("order", "tracking_code", "payment_data")
