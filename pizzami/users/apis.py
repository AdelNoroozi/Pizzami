from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from pizzami.api.mixins import ApiAuthMixin, BasePermissionsMixin
from pizzami.authentication.permissions import IsAuthenticatedAndNotAdmin
from pizzami.users.documentations import GET_ADDRESSES_RESPONSES, CREATE_ADDRESS_RESPONSES
from pizzami.users.serializers import RegisterInputSerializer, RegisterOutputSerializer, ProfileOutputSerializer, \
    AddressInputSerializer
from pizzami.users.services import register, get_profile, get_my_addresses, create_address


class ProfileApi(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "GET": [IsAuthenticated]
    }

    @extend_schema(
        tags=['Users'],
        responses=ProfileOutputSerializer)
    def get(self, request):
        profile_data = get_profile(user=request.user)
        return Response(profile_data, status=status.HTTP_200_OK)


class RegisterApi(APIView):

    @extend_schema(tags=['Users'], request=RegisterInputSerializer, responses=RegisterOutputSerializer)
    def post(self, request):
        register_data = register(data=request.data)

        return Response(register_data, status=status.HTTP_201_CREATED)


class MyAddressesAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "GET": [IsAuthenticatedAndNotAdmin],
        "POST": [IsAuthenticatedAndNotAdmin]
    }

    @extend_schema(
        tags=['Users'],
        responses=GET_ADDRESSES_RESPONSES
    )
    def get(self, request):
        data = get_my_addresses(user=request.user)
        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Users'],
        request=AddressInputSerializer,
        responses=CREATE_ADDRESS_RESPONSES
    )
    def post(self, request):
        data = create_address(data=request.data, user=request.user)
        return Response(data, status=status.HTTP_201_CREATED)
