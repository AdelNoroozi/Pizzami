import uuid

from django.http import QueryDict
from rest_framework.generics import get_object_or_404
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList

from pizzami.feedback.filters import CommentFilter
from pizzami.feedback.models import Comment
from pizzami.feedback.selectors import get_comments as get_comments_selector, search_comment, order_comments, \
    delete_comment as delete_comment_selector
from pizzami.feedback.serializers import CommentInputSerializer, CommentBaseOutputSerializer, \
    CommentDetailedOutputSerializer
from pizzami.users.models import BaseUser


def create_comment(data: dict, user: BaseUser) -> ReturnDict[Comment]:
    user_obj = user.profile if not user.is_staff else None
    serializer = CommentInputSerializer(data=data, context={"user": user_obj})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    response_serializer = CommentBaseOutputSerializer(serializer.instance, many=False)
    return response_serializer.data


def get_comments(query_dict: QueryDict, is_user_staff: bool, user: BaseUser = None) -> ReturnList[Comment]:
    user_obj = user.profile if not is_user_staff else None
    queryset = get_comments_selector(user_created=not is_user_staff, user=user_obj)
    search_param = query_dict.get("search")
    order_param = query_dict.get("order_by")
    if search_param:
        queryset = search_comment(queryset=queryset, search_param=search_param)
    if order_param and order_param.lstrip("-") in ["position", "created_at", "updated_at"]:
        queryset = order_comments(queryset=queryset, order_param=order_param)
    queryset = CommentFilter(query_dict, queryset=queryset).qs
    serializer_class = CommentDetailedOutputSerializer if is_user_staff else CommentBaseOutputSerializer
    serializer = serializer_class(queryset, many=True)
    return serializer.data


def confirm_comment(comment_id: uuid, action: str) -> bool | None:
    valid_actions = ["confirm", "reject", "suspend"]
    if action not in valid_actions:
        return False
    comment = get_object_or_404(Comment, id=comment_id)
    if action == "confirm":
        if comment.is_confirmed is not True:
            comment.is_confirmed = True
            comment.save()
            return True
    elif action == "reject":
        if comment.is_confirmed is not False:
            comment.is_confirmed = False
            comment.save()
            return True
    elif action == "suspend":
        if comment.is_confirmed is not None:
            comment.is_confirmed = None
            comment.save()
            return True
    return None


def delete_comment(comment_id: uuid, user: BaseUser):
    if user.is_staff:
        comment = get_object_or_404(Comment, id=comment_id)
    else:
        comment = get_object_or_404(Comment, id=comment_id, user=user.profile)
    delete_comment_selector(comment=comment)
