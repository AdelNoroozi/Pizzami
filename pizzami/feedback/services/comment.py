from django.http import QueryDict
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList

from pizzami.feedback.models import Comment
from pizzami.feedback.selectors import get_comments as get_comments_selector
from pizzami.feedback.serializers import CommentInputSerializer, CommentBaseOutputSerializer, \
    CommentDetailedOutputSerializer
from pizzami.users.models import BaseUser


def create_comment(data: dict, user: BaseUser) -> ReturnDict[Comment]:
    serializer = CommentInputSerializer(data=data, context={"user": user.profile})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    response_serializer = CommentBaseOutputSerializer(serializer.instance, many=False)
    return response_serializer.data


def get_comments(query_dict: QueryDict, is_user_staff: bool, user: BaseUser = None) -> ReturnList[Comment]:
    if not is_user_staff:
        queryset = get_comments_selector(user_created=True, user=user.profile)
        serializer = CommentBaseOutputSerializer(queryset, many=True)
    else:
        queryset = get_comments_selector(user_created=False)
        serializer = CommentDetailedOutputSerializer(queryset, many=True)
    return serializer.data
