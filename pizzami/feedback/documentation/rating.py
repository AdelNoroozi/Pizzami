from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import OpenApiResponse

RATE_FOOD_DESCRIPTION = _("this API is used for rating foods. if user has not rated the specified food, it will rate it"
                          " by the specified rate. else it will update the previous rating. also users can remove "
                          "their rating for a food by rating it a 0.")

RATE_FOOD_200_RESPONSE = OpenApiResponse(
    description=_("food's rating by current user created/updated/deleted successfully.")
)

RATE_FOOD_400_RESPONSE = OpenApiResponse(
    description=_("input values are invalid or don't match the expected format. e.g: the rate is not an integer or "
                  "the food is not a valid UUID.")
)

RATE_FOOD_401_RESPONSE = OpenApiResponse(
    description=_("user is not authenticated")
)

RATE_FOOD_403_RESPONSE = OpenApiResponse(
    description=_("you are not allowed to perform this action on ratings")
)

RATE_FOOD_404_RESPONSE = OpenApiResponse(
    description=_("no food with specified id found in your access zone")
)

RATE_FOOD_RESPONSES = {
    200: RATE_FOOD_200_RESPONSE,
    400: RATE_FOOD_400_RESPONSE,
    401: RATE_FOOD_401_RESPONSE,
    403: RATE_FOOD_403_RESPONSE,
    404: RATE_FOOD_404_RESPONSE
}
