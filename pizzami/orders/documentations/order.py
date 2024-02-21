from drf_spectacular.utils import OpenApiResponse

from pizzami.orders.serializers import OrderDetailedOutputSerializer

CREATE_OR_UPDATE_ORDER_200_RESPONSE = OpenApiResponse(
    response=OrderDetailedOutputSerializer,
    description="order created/updated successfully."
)

CREATE_OR_UPDATE_ORDER_400_RESPONSE = OpenApiResponse(
    description="input values are invalid or don't match the expected format. e.g: discount is invalid or delivery "
                "order has no address."
)

ORDER_401_RESPONSE = OpenApiResponse(
    description="user is not authenticated"
)

ORDER_403_RESPONSE = OpenApiResponse(
    description="you are not allowed to perform this action on orders"
)

CREATE_OR_UPDATE_ORDER_406_RESPONSE = OpenApiResponse(
    description="cart is empty"
)

CREATE_OR_UPDATE_ORDER_RESPONSES = {
    200: CREATE_OR_UPDATE_ORDER_200_RESPONSE,
    400: CREATE_OR_UPDATE_ORDER_400_RESPONSE,
    401: ORDER_401_RESPONSE,
    403: ORDER_403_RESPONSE,
    406: CREATE_OR_UPDATE_ORDER_406_RESPONSE
}

SUBMIT_MY_ORDER_200_RESPONSE = OpenApiResponse(
    description="order submitted successfully."
)

SUBMIT_MY_ORDER_404_RESPONSE = OpenApiResponse(
    description="you don't have an order in 'created' status."
)

SUBMIT_MY_ORDER_406_RESPONSE = OpenApiResponse(
    description="something is wrong with your order. e.g: order's delivery status not determined."
)

SUBMIT_MY_ORDER_RESPONSES = {
    200: SUBMIT_MY_ORDER_200_RESPONSE,
    401: ORDER_401_RESPONSE,
    403: ORDER_403_RESPONSE,
    404: SUBMIT_MY_ORDER_404_RESPONSE,
    406: SUBMIT_MY_ORDER_406_RESPONSE
}