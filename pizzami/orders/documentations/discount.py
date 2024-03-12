from drf_spectacular.utils import OpenApiResponse, OpenApiParameter

from pizzami.orders.serializers import DiscountCompleteOutputSerializer, DiscountBaseOutputSerializer, \
    DiscountPaginatedOutputSerializer

GET_DISCOUNTS_200_RESPONSE = OpenApiResponse(
    response=DiscountPaginatedOutputSerializer(),
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
    OpenApiParameter(name="page_size", description="must be a valid int"),
    OpenApiParameter(name="page", description="must be a valid int"),
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
    description="you are not allowed to perform this action on discounts"
)

CREATE_DISCOUNT_RESPONSES = {
    201: CREATE_DISCOUNT_201_RESPONSE,
    400: SAVE_DISCOUNT_400_RESPONSE,
    401: DISCOUNT_401_RESPONSE,
    403: DISCOUNT_403_RESPONSE,
    404: SAVE_DISCOUNT_404_RESPONSE
}

DISCOUNT_404_RESPONSE = OpenApiResponse(
    description="discount with specified id does not exist"
)

DELETE_DISCOUNT_204_RESPONSE = OpenApiResponse(
    description="discount deleted successfully."
)

DELETE_DISCOUNT_RESPONSES = {
    204: DELETE_DISCOUNT_204_RESPONSE,
    401: DISCOUNT_401_RESPONSE,
    403: DISCOUNT_403_RESPONSE,
    404: DISCOUNT_404_RESPONSE
}

UPDATE_DISCOUNT_200_RESPONSE = OpenApiResponse(
    response=DiscountCompleteOutputSerializer,
    description="discount updated successfully."
)

UPDATE_DISCOUNT_RESPONSES = {
    200: UPDATE_DISCOUNT_200_RESPONSE,
    400: SAVE_DISCOUNT_400_RESPONSE,
    401: DISCOUNT_401_RESPONSE,
    403: DISCOUNT_403_RESPONSE,
    404: SAVE_DISCOUNT_404_RESPONSE
}

INQUIRY_DISCOUNT_200_RESPONSE = OpenApiResponse(
    response=DiscountBaseOutputSerializer,
    description="discount is acceptable."
)

INQUIRY_DISCOUNT_400_RESPONSE = OpenApiResponse(
    description="input values are invalid or don't match the expected format. e.g: code missed or is not string."
)

INQUIRY_DISCOUNT_406_RESPONSE = OpenApiResponse(
    description="discount code is not acceptable. maybe it is invalid, expired, deactivated or belongs to another user."
)

INQUIRY_DISCOUNT_RESPONSES = {
    200: INQUIRY_DISCOUNT_200_RESPONSE,
    400: INQUIRY_DISCOUNT_400_RESPONSE,
    401: DISCOUNT_401_RESPONSE,
    403: DISCOUNT_403_RESPONSE,
    406: INQUIRY_DISCOUNT_406_RESPONSE
}
