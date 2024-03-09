from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiResponse, OpenApiParameter

from pizzami.feedback.serializers import CommentBaseOutputSerializer, CommentDetailedOutputSerializer, \
    CommentPaginatedOutputSerializer

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
    response=CommentPaginatedOutputSerializer(),
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
    OpenApiParameter(name="page_size", description="must be a valid int"),
    OpenApiParameter(name="page", description="must be a valid int"),
    OpenApiParameter(name="is_confirmed", description="must be true or false or null"),
    OpenApiParameter(name="food", description="must be the id of a food"),
    OpenApiParameter(name="user", description="must be the id of a user profile"),
    OpenApiParameter(name="order_by",
                     description="can be position, created_at, updated_at. a - symbol can"
                                 " be added before the param for descending order.")
]

GET_COMMENTS_DESCRIPTION = _("returns a list of comments. normal users can only access their own comments by setting "
                             "the 'set' parameter to 'mine'. staff users can access all comments.")

CHANGE_COMMENT_CONFIRMATION_STATUS_200_RESPONSE = OpenApiResponse(
    response={"message": _("comment confirmed/rejected/suspended successfully")})

CHANGE_COMMENT_CONFIRMATION_STATUS_400_RESPONSE = OpenApiResponse(
    description=_("invalid request, probably due to invalid action or trying to change comment's status to a status "
                  "which the comment is already in.")
)

COMMENT_404_RESPONSE = OpenApiResponse(
    description=_("Comment with specified id not found")
)

CHANGE_COMMENT_CONFIRMATION_STATUS_RESPONSES = {
    200: CHANGE_COMMENT_CONFIRMATION_STATUS_200_RESPONSE,
    400: CHANGE_COMMENT_CONFIRMATION_STATUS_200_RESPONSE,
    401: COMMENT_401_RESPONSE,
    403: COMMENT_403_RESPONSE,
    404: COMMENT_404_RESPONSE
}

CHANGE_COMMENT_CONFIRMATION_STATUS_DESCRIPTION = _("changes comments confirmation status. the action must be confirm, "
                                                   "reject or suspend. only for staff users.")
