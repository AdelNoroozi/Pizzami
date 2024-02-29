from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from pizzami.feedback.models import Comment
from pizzami.foods.serializers import FoodBaseOutputSerializer


class CommentInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("food", "parent", "text")

    def validate_parent(self, value):
        if value.is_confirmed is not True:
            raise ValidationError(_("a comment's parent must be confirmed."))

        return value

    def validate(self, data):
        if data.get("parent") and data.get("parent").food != data.get("food"):
            raise ValidationError(_("a comment's food must be the same as its parent."))

        return data

    def save(self, **kwargs):
        self.validated_data["user"] = self.context.get("user")
        return super().save(**kwargs)


class CommentBaseOutputSerializer(serializers.ModelSerializer):
    food = FoodBaseOutputSerializer(many=False)

    class Meta:
        model = Comment
        fields = ("id", "food", "parent", "text", "created_at", "is_confirmed")
