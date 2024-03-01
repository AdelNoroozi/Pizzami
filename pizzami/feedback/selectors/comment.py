from django.db.models import QuerySet, Q

from pizzami.feedback.models import Comment
from pizzami.users.models import Profile


def get_comments(user_created: bool, user: Profile = None) -> QuerySet[Comment]:
    if user_created:
        return Comment.objects.filter(user=user)
    else:
        return Comment.objects.all()


def search_comment(queryset: QuerySet, search_param: str) -> QuerySet[Comment]:
    return queryset.filter(Q(text__icontains=search_param) | Q(food__name__icontains=search_param)).distinct()


def order_comments(queryset: QuerySet, order_param: str) -> QuerySet[Comment]:
    return queryset.order_by(order_param)
