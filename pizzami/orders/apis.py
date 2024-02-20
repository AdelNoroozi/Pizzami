from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from pizzami.api.mixins import ApiAuthMixin, BasePermissionsMixin
from pizzami.authentication.permissions import IsAuthenticatedAndNotAdmin
from pizzami.orders.documentations import GET_DISCOUNTS_RESPONSES, CREATE_DISCOUNT_RESPONSES, GET_DISCOUNTS_PARAMETERS, \
    DELETE_DISCOUNT_RESPONSES, UPDATE_DISCOUNT_RESPONSES, ADD_TO_CART_RESPONSES, MY_CART_RESPONSES, \
    INQUIRY_DISCOUNT_RESPONSES
from pizzami.orders.selectors import has_discount_orders, get_or_create_cart, inquiry_discount_by_code
from pizzami.orders.serializers import DiscountInputSerializer, CartSerializer, CartItemInputSerializer, \
    DiscountInquirySerializer, DiscountBaseOutputSerializer
from pizzami.orders.services import get_discount_list, create_discount, delete_discount, update_discount, add_to_cart


class DiscountsAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "GET": [IsAuthenticated],
        "POST": [IsAdminUser]
    }

    @extend_schema(
        tags=['Orders'],
        parameters=GET_DISCOUNTS_PARAMETERS,
        responses=GET_DISCOUNTS_RESPONSES
    )
    def get(self, request):
        query_dict = request.GET
        data = get_discount_list(query_dict=query_dict, is_user_staff=request.user.is_staff, user=request.user)
        return Response(data=data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Orders'],
        request=DiscountInputSerializer,
        responses=CREATE_DISCOUNT_RESPONSES
    )
    def post(self, request):
        discount_data = create_discount(request.data)
        return Response(data=discount_data, status=status.HTTP_201_CREATED)


class DiscountAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    @extend_schema(
        tags=['Orders'],
        responses=DELETE_DISCOUNT_RESPONSES
    )
    def delete(self, request, **kwargs):
        _id = kwargs.get("id")
        if has_discount_orders(discount_id=_id):
            return Response(data={"message": _(
                "can't delete this discount cause there are orders referring to it.")},
                status=status.HTTP_400_BAD_REQUEST)
        delete_discount(discount_id=_id)
        return Response(data={"message": "done"}, status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        tags=['Orders'],
        request=DiscountInputSerializer,
        responses=UPDATE_DISCOUNT_RESPONSES
    )
    def put(self, request, **kwargs):
        _id = kwargs.get("id")
        updated_discount_data = update_discount(discount_id=_id, data=request.data)
        return Response(data=updated_discount_data, status=status.HTTP_200_OK)


class InquiryDiscountAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "POST": [IsAuthenticatedAndNotAdmin]
    }

    @extend_schema(
        tags=['Orders'],
        request=DiscountInquirySerializer,
        responses=INQUIRY_DISCOUNT_RESPONSES
    )
    def post(self, request, **kwargs):
        serializer = DiscountInquirySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        discount = inquiry_discount_by_code(code=serializer.data["code"], user=request.user.profile)
        if discount is None:
            return Response(data={"message": "invalid code"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        response_serializer = DiscountBaseOutputSerializer(discount, many=False)
        return Response(data=response_serializer.data, status=status.HTTP_200_OK)


class AddToCartAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "PUT": [IsAuthenticatedAndNotAdmin]
    }

    @extend_schema(
        tags=['Orders'],
        request=CartItemInputSerializer,
        responses=ADD_TO_CART_RESPONSES
    )
    def put(self, request, **kwargs):
        serializer = CartItemInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = add_to_cart(food_id=serializer.data["food_id"], count=serializer.data["count"], user=request.user)
        response_serializer = CartSerializer(cart, many=False)
        return Response(data=response_serializer.data, status=status.HTTP_200_OK)


class MyCartAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "GET": [IsAuthenticatedAndNotAdmin]
    }

    @extend_schema(
        tags=['Orders'],
        responses=MY_CART_RESPONSES
    )
    def get(self, request, **kwargs):
        cart = get_or_create_cart(user=request.user.profile)
        serializer = CartSerializer(cart, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
