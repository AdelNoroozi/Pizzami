from rest_framework.utils.serializer_helpers import ReturnDict

from pizzami.feedback.models import Comment
from pizzami.feedback.serializers import CommentInputSerializer, CommentBaseOutputSerializer
from pizzami.users.models import BaseUser


def create_comment(data: dict, user: BaseUser) -> ReturnDict[Comment]:
    serializer = CommentInputSerializer(data=data, context={"user": user.profile})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    response_serializer = CommentBaseOutputSerializer(serializer.instance, many=False)
    return response_serializer.data
