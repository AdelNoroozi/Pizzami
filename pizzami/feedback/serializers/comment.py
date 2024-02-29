from rest_framework import serializers

from pizzami.feedback.models import Comment


class CommentInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("food", "parent", "text")

    def save(self, **kwargs):
        self.validated_data["user"] = self.context.get("user")
        return super().save(**kwargs)
