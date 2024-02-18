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



