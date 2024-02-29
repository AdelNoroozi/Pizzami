from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiResponse

from pizzami.feedback.serializers import CommentBaseOutputSerializer

CREATE_COMMENT_200_RESPONSE = OpenApiResponse(
    response=CommentBaseOutputSerializer,
    description=_("comment created successfully.")
)

CREATE_COMMENT_400_RESPONSE = OpenApiResponse(
    description=_(
        "input values are invalid or don't match the expected format. e.g: active food with that id does not exist in"
        " public access zone. parent does not exist, is not for the same food or is not confirmed.")
)

COMMENT_401_RESPONSE = OpenApiResponse(
    description=_("user is not authenticated")
)

COMMENT_403_RESPONSE = OpenApiResponse(
    description=_("you are not allowed to perform this action on comments")
)

CREATE_COMMENT_RESPONSES = {
    201: CREATE_COMMENT_200_RESPONSE,
    400: CREATE_COMMENT_400_RESPONSE,
    401: COMMENT_401_RESPONSE,
    403: COMMENT_403_RESPONSE
}
