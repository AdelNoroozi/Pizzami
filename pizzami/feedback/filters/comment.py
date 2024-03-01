from django_filters import FilterSet

from pizzami.feedback.models import Comment


class CommentFilter(FilterSet):
    class Meta:
        model = Comment
        fields = {
            "food": ["exact"],
            "user": ["exact"],
            "is_confirmed": ["exact"]
        }
