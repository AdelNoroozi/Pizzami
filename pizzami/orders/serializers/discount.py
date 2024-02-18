from rest_framework import serializers

from pizzami.orders.models import Discount


class DiscountBaseOutputSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()

    class Meta:
        model = Discount
        fields = ("id", "name", "description", "code", "expiration_date", "value")

    def get_value(self, obj: Discount) -> str:
        if obj.type == obj.TYPE_RATIO:
            return f"{obj.percentage_value}%"
        else:
            return f"{obj.absolute_value}$"


class DiscountCompleteOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = "__all__"
