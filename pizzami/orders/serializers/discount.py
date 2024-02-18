from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from pizzami.foods.models import Food, FoodCategory
from pizzami.foods.serializers import FoodBaseOutputSerializer, FoodCategoryBaseOutputSerializer
from pizzami.orders.models import Discount
from pizzami.users.models import Profile
from pizzami.users.serializers import ProfileReferenceSerializer


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


class SpecifiedToRelatedField(serializers.RelatedField):

    def to_representation(self, value):
        if isinstance(value, Food):
            serializer = FoodBaseOutputSerializer(value)
        elif isinstance(value, Profile):
            serializer = ProfileReferenceSerializer(value)
        elif isinstance(value, FoodCategory):
            serializer = FoodCategoryBaseOutputSerializer(value)
        else:
            return None
        return serializer.data


class DiscountCompleteOutputSerializer(serializers.ModelSerializer):
    specified_to = SpecifiedToRelatedField(source="specified_object", read_only=True)

    class Meta:
        model = Discount
        exclude = ("object_id", "specified_type")


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

    @transaction.atomic
    def create(self, validated_data):
        specified_to_type_dict = {
            "USR": Profile,
            "FOD": Food,
            "CAT": FoodCategory
        }
        specified_to_type = validated_data.get("specified_to_type")
        specified_object = get_object_or_404(specified_to_type_dict[specified_to_type], id=validated_data["object_id"])
        validated_data.pop("object_id")
        validated_data["specified_object"] = specified_object
        return super().create(validated_data)
