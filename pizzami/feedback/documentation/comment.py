from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiResponse, OpenApiParameter

from pizzami.feedback.serializers import CommentBaseOutputSerializer, CommentDetailedOutputSerializer

CREATE_COMMENT_201_RESPONSE = OpenApiResponse(
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
    201: CREATE_COMMENT_201_RESPONSE,
    400: CREATE_COMMENT_400_RESPONSE,
    401: COMMENT_401_RESPONSE,
    403: COMMENT_403_RESPONSE
}

GET_COMMENTS_200_RESPONSE = OpenApiResponse(
    response=CommentDetailedOutputSerializer(many=True),
    description=_("returns a list of comments. the user field is only shown to staff users.")
)

GET_COMMENTS_RESPONSES = {
    200: GET_COMMENTS_200_RESPONSE,
    401: COMMENT_401_RESPONSE,
    403: COMMENT_403_RESPONSE
}

GET_COMMENTS_PARAMETERS = [
    OpenApiParameter(name="set", description="can be null or mine."),
    OpenApiParameter(name="search",
                     description="can be any string. this will be done on comment's text or food's name."),
    OpenApiParameter(name="is_confirmed", description="must be true or false or null"),
    OpenApiParameter(name="food", description="must be the id of a food"),
    OpenApiParameter(name="user", description="must be the id of a user profile"),
    OpenApiParameter(name="order_by",
                     description="can be position, created_at, modified_at. a - symbol can"
                                 " be added before the param for descending order.")
]

GET_COMMENTS_DESCRIPTION = _("returns a list of comments. normal users can only access their own comments by setting "
                             "the 'set' parameter to 'mine'. staff users can access all comments.")
