from drf_spectacular.utils import OpenApiResponse, OpenApiParameter

from pizzami.orders.serializers import DiscountCompleteOutputSerializer

GET_DISCOUNTS_200_RESPONSE = OpenApiResponse(
    response=DiscountCompleteOutputSerializer(many=True),
    description="Represents a list of discounts. For Staff users, it shows all of the discounts but for normal users "
                "just the discounts that are specified to them. Also the representation for normal users only contains"
                " the id, name, description, code, exp dat and value of the discount, but for staff users it contains "
                "every single field."
)

DISCOUNT_401_RESPONSE = OpenApiResponse(
    description="user is not authenticated"
)

GET_DISCOUNTS_RESPONSES = {
    200: GET_DISCOUNTS_200_RESPONSE,
    401: DISCOUNT_401_RESPONSE
}

GET_DISCOUNTS_PARAMETERS = [
    OpenApiParameter(name="search", description="can be any string"),
    OpenApiParameter(name="is_active", description="must be true or false"),
    OpenApiParameter(name="is_public", description="must be true or false"),
    OpenApiParameter(name="has_time_limit", description="must be true or false"),
    OpenApiParameter(name="type", description="must be ABS (absolute) or RAT (ratio)"),
    OpenApiParameter(name="specified_to_type", description="must be USR (user), FOD (food) or CAT (food category)"),
    OpenApiParameter(name="order_by", description="can be start_date, expiration_date, position, created_at, "
                                                  "modified_at, absolute_value, percentage_value. a - symbol can be "
                                                  "added before the param for descending order."),
]

CREATE_DISCOUNT_201_RESPONSE = OpenApiResponse(
    response=DiscountCompleteOutputSerializer,
    description="a new discount created successfully."
)

SAVE_DISCOUNT_400_RESPONSE = OpenApiResponse(
    description="input values are invalid or don't match the expected format. e.g: discount type is absolute, but "
                "absolute value is null."
)

SAVE_DISCOUNT_404_RESPONSE = OpenApiResponse(
    description="no specified object found for this specified id for the specified type"
)

DISCOUNT_403_RESPONSE = OpenApiResponse(
    description="you are not allowed to perform this action"
)

CREATE_DISCOUNT_RESPONSES = {
    201: CREATE_DISCOUNT_201_RESPONSE,
    400: SAVE_DISCOUNT_400_RESPONSE,
    401: DISCOUNT_401_RESPONSE,
    403: DISCOUNT_403_RESPONSE,
    404: SAVE_DISCOUNT_404_RESPONSE
}
