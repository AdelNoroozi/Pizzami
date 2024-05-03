from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from pizzami.api.mixins import ApiAuthMixin, BasePermissionsMixin
from pizzami.api.pagination import FullPagination
from pizzami.authentication.permissions import IsAuthenticatedAndNotAdmin, IsSuperUser
from pizzami.common.services import change_activation_status
from pizzami.users.documentations import GET_ADDRESSES_RESPONSES, CREATE_ADDRESS_RESPONSES, UPDATE_ADDRESS_RESPONSES, \
    DELETE_ADDRESS_RESPONSES, GET_USERS_PARAMETERS, REQUEST_PASSWORD_RESPONSES, RESET_PASSWORD_RESPONSES, \
    CHANGE_PASSWORD_RESPONSES
from pizzami.users.models import BaseUser, Profile
from pizzami.users.serializers import RegisterInputSerializer, RegisterOutputSerializer, ProfileBaseOutputSerializer, \
    AddressInputSerializer, AdminInputSerializer, UserPaginatedOutputSerializer, \
    RequestPasswordResetSerializer, ResetPasswordSerializer, ProfileUpdateSerializer, ProfileFullOutputSerializer, \
    ProfilePageOutputSerializer
from pizzami.users.serializers.user import ChangePasswordSerializer
from pizzami.users.services import register, get_profile, get_my_addresses, create_address, update_address, \
    delete_address, create_admin, get_users, request_password_reset, reset_password, change_password, update_profile, \
    get_full_profile


class SelfProfileApi(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "GET": [IsAuthenticatedAndNotAdmin]
    }

    @extend_schema(
        tags=['Users:Users'],
        responses=ProfileBaseOutputSerializer,
        parameters=[OpenApiParameter(name="full", description="must be 'yes' or null")])
    def get(self, request):
        if request.GET.get("full") == "yes":
            profile_data = get_full_profile(profile=request.user.profile, is_self=True)
        else:
            profile_data = get_profile(user=request.user)
        return Response(profile_data, status=status.HTTP_200_OK)


class ProfileApi(APIView):

    @extend_schema(
        tags=['Users:Profiles'],
        responses=ProfilePageOutputSerializer)
    def get(self, request, **kwargs):
        _id = kwargs.get("id")
        profile = get_object_or_404(Profile, id=_id, user__is_active=True)
        profile_data = get_full_profile(profile=profile, is_self=False)
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

    @extend_schema(tags=['Users:Users'], parameters=GET_USERS_PARAMETERS, responses=UserPaginatedOutputSerializer())
    def get(self, request):
        data = get_users(query_dict=request.GET, is_superuser=request.user.is_superuser)
        paginator = FullPagination()
        paginated_data = paginator.paginate_queryset(queryset=data, request=request)
        return paginator.get_paginated_response(data={"ok": True, "data": paginated_data, "status": status.HTTP_200_OK})


class UserActivateAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "PATCH": [IsAdminUser]
    }

    @extend_schema(
        tags=['Users:Users'],
        description="changes user's activation status. only for staff users.")
    def patch(self, request, **kwargs):
        user_id = kwargs.get("id")
        queryset = BaseUser.objects.exclude(id=request.user.id) if request.user.is_superuser else BaseUser.objects.filter(is_admin=False, is_superuser=False)
        new_activation_status = change_activation_status(obj_id=user_id, queryset=queryset)
        activation_str = "activated" if new_activation_status else "deactivated"
        return Response(data={"message": f"user {activation_str} successfully"})


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


class UpdateProfileAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "PUT": [IsAuthenticatedAndNotAdmin]
    }

    @extend_schema(
        tags=['Users:Users'],
        request=ProfileUpdateSerializer,
        responses=ProfileFullOutputSerializer
    )
    def put(self, request, **kwargs):
        data = update_profile(user=request.user, data=request.data)
        return Response(data=data, status=status.HTTP_200_OK)


class ChangePasswordAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "POST": [IsAuthenticated]
    }

    @extend_schema(
        tags=['Users:Password'],
        request=ChangePasswordSerializer,
        responses=CHANGE_PASSWORD_RESPONSES
    )
    def post(self, request, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        change_password(user=request.user, password=serializer.data.get("password"))
        return Response({"message": "password changed successfully"}, status=status.HTTP_200_OK)


class RequestPasswordResetAPI(APIView):
    @extend_schema(
        tags=['Users:Password'],
        request=RequestPasswordResetSerializer,
        responses=REQUEST_PASSWORD_RESPONSES
    )
    def post(self, request):
        serializer = RequestPasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get("email")
        if request_password_reset(email=email):
            return Response({"message": f"password reset link sent to {email}"}, status=status.HTTP_200_OK)
        return Response(data={"error": "something went wrong"}, status=status.HTTP_408_REQUEST_TIMEOUT)


class ResetPasswordAPI(APIView):
    @extend_schema(
        tags=['Users:Password'],
        request=ResetPasswordSerializer,
        responses=RESET_PASSWORD_RESPONSES
    )
    def post(self, request, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if reset_password(uid=kwargs.get("uid"), token=kwargs.get("token"), password=serializer.data.get("password")):
            return Response({"message": "password changed successfully"}, status=status.HTTP_200_OK)
        return Response({"message": "invalid or expired token"}, status=status.HTTP_403_FORBIDDEN)


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
