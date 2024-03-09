from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from pizzami.api.mixins import ApiAuthMixin, BasePermissionsMixin
from pizzami.authentication.permissions import IsAuthenticatedAndNotAdmin, IsSuperUser
from pizzami.users.documentations import GET_ADDRESSES_RESPONSES, CREATE_ADDRESS_RESPONSES, UPDATE_ADDRESS_RESPONSES, \
    DELETE_ADDRESS_RESPONSES
from pizzami.users.serializers import RegisterInputSerializer, RegisterOutputSerializer, ProfileOutputSerializer, \
    AddressInputSerializer, AdminInputSerializer, UserOutputSerializer
from pizzami.users.services import register, get_profile, get_my_addresses, create_address, update_address, \
    delete_address, create_admin, get_users


class ProfileApi(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "GET": [IsAuthenticatedAndNotAdmin]
    }

    @extend_schema(
        tags=['Users:Users'],
        responses=ProfileOutputSerializer)
    def get(self, request):
        profile_data = get_profile(user=request.user)
        return Response(profile_data, status=status.HTTP_200_OK)


class RegisterApi(APIView):

    @extend_schema(tags=['Users:Users'], request=RegisterInputSerializer, responses=RegisterOutputSerializer)
    def post(self, request):
        register_data = register(data=request.data)

        return Response(register_data, status=status.HTTP_201_CREATED)


class UsersAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "GET": [IsAdminUser]
    }

    @extend_schema(tags=['Users:Users'], responses=UserOutputSerializer(many=True))
    def get(self, request):
        data = get_users(is_superuser=request.user.is_superuser)
        return Response(data, status=status.HTTP_200_OK)


class CreateAdmin(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "POST": [IsSuperUser]
    }

    @extend_schema(tags=['Users:Admins'], request=AdminInputSerializer)
    def post(self, request):
        create_admin(data=request.data)
        return Response({"email": request.data.get("email")}, status=status.HTTP_201_CREATED)


class MyAddressesAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "GET": [IsAuthenticatedAndNotAdmin],
        "POST": [IsAuthenticatedAndNotAdmin]
    }

    @extend_schema(
        tags=['Users:Addresses'],
        parameters=[OpenApiParameter(name="search", description="can be any string.")],
        responses=GET_ADDRESSES_RESPONSES
    )
    def get(self, request):
        search_param = request.GET.get("search")
        data = get_my_addresses(user=request.user, search_param=search_param)
        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Users:Addresses'],
        request=AddressInputSerializer,
        responses=CREATE_ADDRESS_RESPONSES
    )
    def post(self, request):
        data = create_address(data=request.data, user=request.user)
        return Response(data, status=status.HTTP_201_CREATED)


class MyAddressAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "PUT": [IsAuthenticatedAndNotAdmin],
        "DELETE": [IsAuthenticatedAndNotAdmin]
    }

    @extend_schema(
        tags=['Users:Addresses'],
        request=AddressInputSerializer,
        responses=UPDATE_ADDRESS_RESPONSES
    )
    def put(self, request, **kwargs):
        _id = kwargs.get("id")
        data = update_address(address_id=_id, data=request.data, user=request.user)
        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Users:Addresses'],
        responses=DELETE_ADDRESS_RESPONSES
    )
    def delete(self, request, **kwargs):
        _id = kwargs.get("id")
        delete_address(address_id=_id, user=request.user)
        return Response({"message": "done"}, status=status.HTTP_204_NO_CONTENT)
