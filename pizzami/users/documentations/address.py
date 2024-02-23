from drf_spectacular.utils import OpenApiResponse

from pizzami.users.serializers import AddressOutputSerializer

GET_ADDRESSES_200_RESPONSE = OpenApiResponse(
    response=AddressOutputSerializer(many=True),
    description="Represents a list of user's addresses. only normal users can perform this action."
)

ADDRESSES_401_RESPONSE = OpenApiResponse(
    description="user is not authenticated."
)

ADDRESSES_403_RESPONSE = OpenApiResponse(
    description="you don't have the privilege to perform ths action on addresses."
)

GET_ADDRESSES_RESPONSES = {
    200: GET_ADDRESSES_200_RESPONSE,
    401: ADDRESSES_401_RESPONSE,
    403: ADDRESSES_403_RESPONSE
}

CREATE_ADDRESS_201_RESPONSE = OpenApiResponse(
    response=AddressOutputSerializer(many=False),
    description="address created successfully."
)

SAVE_ADDRESS_400_RESPONSE = OpenApiResponse(
    description="input values are invalid or don't match the expected format. e.g: phone number is invalid."
)

CREATE_ADDRESS_RESPONSES = {
    201: CREATE_ADDRESS_201_RESPONSE,
    400: SAVE_ADDRESS_400_RESPONSE,
    401: ADDRESSES_401_RESPONSE,
    403: ADDRESSES_403_RESPONSE
}

UPDATE_ADDRESS_200_RESPONSE = OpenApiResponse(
    response=AddressOutputSerializer(many=False),
    description="address updated successfully."
)

ADDRESS_404_RESPONSE = OpenApiResponse(
    description="no address with specified id found in your access zone."
)

UPDATE_ADDRESS_RESPONSES = {
    200: UPDATE_ADDRESS_200_RESPONSE,
    400: SAVE_ADDRESS_400_RESPONSE,
    401: ADDRESSES_401_RESPONSE,
    403: ADDRESSES_403_RESPONSE,
    404: ADDRESS_404_RESPONSE
}
