from django.db.models import QuerySet

from pizzami.feedback.models import Comment
from pizzami.users.models import Profile


def get_comments(user_created: bool, user: Profile = None) -> QuerySet(Comment):
    if user_created:
        return Comment.objects.filter(user=user)
    else:
        return Comment.objects.all()
