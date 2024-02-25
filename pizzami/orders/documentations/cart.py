from drf_spectacular.utils import OpenApiResponse

from pizzami.orders.serializers import CartSerializer

ADD_TO_CART_200_RESPONSE = OpenApiResponse(
    response=CartSerializer,
    description="item added/removed to/from cart successfully."
)

ADD_TO_CART_400_RESPONSE = OpenApiResponse(
    description="input values are invalid or don't match the expected format. e.g: count is not an int or food_id is"
                "not a valid uuid."
)

CART_401_RESPONSE = OpenApiResponse(
    description="user is not authenticated"
)

CART_403_RESPONSE = OpenApiResponse(
    description="you are not allowed to perform this action on carts"
)

ADD_TO_CART_404_RESPONSE = OpenApiResponse(
    description="food with specified id does not exist"
)

ADD_TO_CART_406_RESPONSE = OpenApiResponse(
    description="food is unavailable."
)

ADD_TO_CART_RESPONSES = {
    200: ADD_TO_CART_200_RESPONSE,
    400: ADD_TO_CART_400_RESPONSE,
    401: CART_401_RESPONSE,
    403: CART_403_RESPONSE,
    404: ADD_TO_CART_404_RESPONSE,
    406: ADD_TO_CART_406_RESPONSE
}

MY_CART_200_RESPONSE = OpenApiResponse(
    response=CartSerializer,
    description="users current alive cart."
)

MY_CART_RESPONSES = {
    200: MY_CART_200_RESPONSE,
    401: CART_401_RESPONSE,
    403: CART_403_RESPONSE,
}
