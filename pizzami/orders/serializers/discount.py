from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from pizzami.foods.models import Food, FoodCategory
from pizzami.orders.models import Discount
from pizzami.users.models import Profile


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


class DiscountInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        exclude = ("id", "is_active", "position", "created_at", "modified_at", "specified_type")

    def validate(self, data):
        if data["has_time_limit"] and (data["start_date"] is None or data["expiration_date"] is None):
            raise ValidationError(_("time limited discounts must have start and expiration date"))

        if data["type"] == Discount.TYPE_ABSOLUTE and data["absolute_value"] is None:
            raise ValidationError(_("absolute discounts must have a absolute value"))

        if data["type"] == Discount.TYPE_RATIO and data["percentage_value"] is None:
            raise ValidationError(_("ratio discounts must have a percentage value"))

        if (data["specified_to_type"] == Discount.SPECIFIED_TO_USER and
            not isinstance(data["specified_object"], Profile)) or (
                data["specified_to_type"] == Discount.SPECIFIED_TO_FOOD and
                not isinstance(data["specified_object"], Food)) or (
                data["specified_to_type"] == Discount.SPECIFIED_TO_CATEGORY and
                not isinstance(data["specified_object"], FoodCategory)
        ):
            raise ValidationError(_(f"the specified id must be a type of {data['specified_to_type']}"))
