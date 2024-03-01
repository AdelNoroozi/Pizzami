from django.http import QueryDict
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList

from pizzami.feedback.filters import CommentFilter
from pizzami.feedback.models import Comment
from pizzami.feedback.selectors import get_comments as get_comments_selector, search_comment
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
    user_obj = user.profile if not is_user_staff else None
    queryset = get_comments_selector(user_created=not is_user_staff, user=user_obj)
    search_param = query_dict.get("search")
    if search_param:
        queryset = search_comment(queryset=queryset, search_param=search_param)
    queryset = CommentFilter(query_dict, queryset=queryset).qs
    serializer_class = CommentDetailedOutputSerializer if is_user_staff else CommentBaseOutputSerializer
    serializer = serializer_class(queryset, many=True)
    return serializer.data
