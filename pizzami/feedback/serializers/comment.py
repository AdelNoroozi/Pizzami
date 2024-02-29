from rest_framework import serializers

from pizzami.feedback.models import Comment
from pizzami.foods.serializers import FoodBaseOutputSerializer


class CommentInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("food", "parent", "text")

    def save(self, **kwargs):
        self.validated_data["user"] = self.context.get("user")
        return super().save(**kwargs)


class CommentBaseOutputSerializer(serializers.ModelSerializer):
    food = FoodBaseOutputSerializer(many=False)

    class Meta:
        model = Comment
        fields = ("id", "food", "parent", "text", "created_at", "is_confirmed")
