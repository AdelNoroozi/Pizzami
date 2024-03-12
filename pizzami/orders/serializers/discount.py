from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from pizzami.common.serializers import PaginatedOutputSerializer
from pizzami.foods.models import Food, FoodCategory
from pizzami.foods.serializers import FoodBaseOutputSerializer, FoodCategoryBaseOutputSerializer
from pizzami.orders.models import Discount
from pizzami.orders.selectors import deactivate_discounts_by_obj
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
        exclude = ("id", "position", "created_at", "updated_at", "specified_type")

    def validate(self, data):
        if data.get("has_time_limit") is True and (
                data.get("start_date") is None or data.get("expiration_date") is None):
            raise ValidationError(_("time limited discounts must have start and expiration date"))

        if data.get("type") == Discount.TYPE_ABSOLUTE and data.get("absolute_value") is None:
            raise ValidationError(_("absolute discounts must have a absolute value"))

        if data.get("type") == Discount.TYPE_RATIO and data.get("percentage_value") is None:
            raise ValidationError(_("ratio discounts must have a percentage value"))

        if data.get("specified_to_type") == Discount.SPECIFIED_TO_USER or data.get("specified_to_type") is None:
            if not data.get("code"):
                raise ValidationError(_("User-specified or public broad discounts must have a code."))
        else:
            if data.get("code"):
                raise ValidationError(_("Food or food category specified discounts must not have a code."))

        if data.get("specified_to_type") == Discount.SPECIFIED_TO_USER and data.get("is_public"):
            raise ValidationError(_("user specified discounts can not be public."))

        return data

    @transaction.atomic
    def save(self, **kwargs):
        validated_data = self.validated_data
        specified_to_type_dict = {
            "USR": Profile,
            "FOD": Food,
            "CAT": FoodCategory
        }
        specified_to_type = validated_data.get("specified_to_type")
        specified_object = get_object_or_404(specified_to_type_dict[specified_to_type], id=validated_data["object_id"])
        object_id = validated_data.pop("object_id")
        if (validated_data.get("is_active") is None or validated_data.get("is_active") is True) and (
                specified_to_type == "FOD" or specified_to_type == "CAT"):
            deactivate_discounts_by_obj(object_id=object_id)
        validated_data["specified_object"] = specified_object
        return super().save(**kwargs)


class DiscountInquirySerializer(serializers.Serializer):
    code = serializers.CharField(required=True)


class DiscountPaginatedOutputSerializer(PaginatedOutputSerializer):
    class ResultsOutputSerializer(PaginatedOutputSerializer.ResultsOutputSerializer):
        data = DiscountCompleteOutputSerializer(many=True)

    results = ResultsOutputSerializer(many=False)
