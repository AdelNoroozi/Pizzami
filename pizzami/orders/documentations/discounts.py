from drf_spectacular.utils import OpenApiResponse

from pizzami.orders.serializers import DiscountCompleteOutputSerializer

GET_DISCOUNTS_200_RESPONSE = OpenApiResponse(
    response=DiscountCompleteOutputSerializer(many=True),
    description="Represents a list of discounts. For Staff users, it shows all of the discounts but for normal users"
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
