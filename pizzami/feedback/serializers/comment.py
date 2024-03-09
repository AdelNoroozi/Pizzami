from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from pizzami.common.serializers import PaginatedOutputSerializer
from pizzami.feedback.models import Comment
from pizzami.foods.serializers import FoodBaseOutputSerializer
from pizzami.users.serializers import ProfileReferenceSerializer


class CommentInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("food", "parent", "text")

    def validate_food(self, value):
        if not value.is_active or not value.is_confirmed or not value.is_public:
            raise ValidationError(_(f"Invalid pk \"{value.id}\" - object does not exist."))

        return value

    def validate_parent(self, value):
        if value.is_confirmed is not True:
            raise ValidationError(_("a comment's parent must be confirmed."))

        return value

    def validate(self, data):
        if data.get("parent") and data.get("parent").food != data.get("food"):
            raise ValidationError(_("a comment's food must be the same as its parent."))

        return data

    def save(self, **kwargs):
        user_obj = self.context.get("user")
        if user_obj:
            self.validated_data["user"] = user_obj
        else:
            self.validated_data["by_staff"] = True
            self.validated_data["is_confirmed"] = True
        return super().save(**kwargs)


class CommentBaseOutputSerializer(serializers.ModelSerializer):
    food = FoodBaseOutputSerializer(many=False)

    class Meta:
        model = Comment
        fields = ("id", "food", "parent", "text", "created_at", "updated_at", "is_confirmed")


class CommentDetailedOutputSerializer(CommentBaseOutputSerializer):
    user = ProfileReferenceSerializer(many=False)

    class Meta(CommentBaseOutputSerializer.Meta):
        fields = CommentBaseOutputSerializer.Meta.fields + ("user", "by_staff")


class CommentHierarchicalOutputSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        exclude = ("id", "food", "parent", "is_confirmed")

    def get_user(self, obj):
        user = obj.user
        return user.public_name if user else None

    def get_children(self, obj):
        serializer = CommentHierarchicalOutputSerializer(obj.children, many=True)
        return serializer.data


class CommentPaginatedOutputSerializer(PaginatedOutputSerializer):
    class ResultsOutputSerializer(PaginatedOutputSerializer.ResultsOutputSerializer):
        data = CommentDetailedOutputSerializer(many=True)

    results = ResultsOutputSerializer(many=False)
