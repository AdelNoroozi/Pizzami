from drf_spectacular.utils import OpenApiResponse, OpenApiParameter

from pizzami.orders.serializers import OrderDetailedOutputSerializer, OrderBaseOutputSerializer

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


UPDATE_ORDER_STATUS_200_RESPONSE = OpenApiResponse(
    description="order status updated successfully."
)

UPDATE_ORDER_STATUS_400_RESPONSE = OpenApiResponse(
    description="input values are invalid or don't match the expected format. e.g: input status is neither 'IPR', 'RJC'"
                ", nor 'DLV'."
)

UPDATE_ORDER_STATUS_404_RESPONSE = OpenApiResponse(
    description="order with this id not found."
)

UPDATE_ORDER_STATUS_406_RESPONSE = OpenApiResponse(
    description="something about this order makes it impossible to change its status. e.g: maybe it has not been paid"
                " for yet or is delivered/rejected before or ir is already in that status."
)

UPDATE_ORDER_STATUS_RESPONSES = {
    200: UPDATE_ORDER_STATUS_200_RESPONSE,
    400: UPDATE_ORDER_STATUS_400_RESPONSE,
    401: ORDER_401_RESPONSE,
    403: ORDER_403_RESPONSE,
    404: UPDATE_ORDER_STATUS_404_RESPONSE,
    406: UPDATE_ORDER_STATUS_406_RESPONSE
}


GET_ORDERS_PARAMETERS = [
    OpenApiParameter(name="set", description="can be null or mine."),
    OpenApiParameter(name="search", description="can be any string. this will be done on addresses, foods' name, "
                                                "foods' category & user's name."),
]

GET_ORDERS_200_RESPONSE = OpenApiResponse(
    response=OrderBaseOutputSerializer(many=True),
    description="returns a list of orders. only staff users can access all of the orders. non staff users can only "
                "access their own orders which can be done by setting the value for parameter 'set' to 'mine'."
)

GET_ORDERS_RESPONSES = {
    200: GET_ORDERS_200_RESPONSE,
    401: ORDER_401_RESPONSE,
    403: ORDER_403_RESPONSE
}
