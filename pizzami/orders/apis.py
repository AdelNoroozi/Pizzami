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
    INQUIRY_DISCOUNT_RESPONSES, CREATE_OR_UPDATE_ORDER_RESPONSES, SUBMIT_MY_ORDER_RESPONSES, \
    UPDATE_ORDER_STATUS_RESPONSES, GET_ORDERS_RESPONSES, GET_ORDERS_PARAMETERS
from pizzami.orders.selectors import has_discount_orders, get_or_create_cart, inquiry_discount_by_code
from pizzami.orders.serializers import DiscountInputSerializer, CartSerializer, CartItemInputSerializer, \
    DiscountInquirySerializer, DiscountBaseOutputSerializer, OrderInputSerializer, PaymentGenericSerializer, \
    UpdateOrderStatusSerializer
from pizzami.orders.services import get_discount_list, create_discount, delete_discount, update_discount, add_to_cart, \
    create_or_update_order, submit_my_order, create_payment, update_order_status, get_orders


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


class OrdersAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "GET": [IsAuthenticated],
        "PUT": [IsAuthenticatedAndNotAdmin]
    }

    @extend_schema(
        tags=['Orders'],
        request=OrderInputSerializer,
        responses=CREATE_OR_UPDATE_ORDER_RESPONSES
    )
    def put(self, request, **kwargs):
        order_data = create_or_update_order(data=request.data, user=request.user)
        if order_data is None:
            return Response(data={"error": "cart is empty"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(data=order_data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Orders'],
        parameters=GET_ORDERS_PARAMETERS,
        responses=GET_ORDERS_RESPONSES
    )
    def get(self, request):
        query_dict = request.GET
        user = request.user
        if not query_dict.get("set") == "mine":
            if not user.is_staff:
                return Response(data={"error": "non staff users can only access their own orders"},
                                status=status.HTTP_403_FORBIDDEN)
            data = get_orders(query_dict=query_dict, user_created=False)
        else:
            if user.is_staff:
                return Response(data={"error": "only authenticated normal users can access their own orders"},
                                status=status.HTTP_403_FORBIDDEN)
            data = get_orders(query_dict=query_dict, user_created=True, user=user)
        return Response(data=data, status=status.HTTP_200_OK)


class OrderAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "GET": [IsAuthenticated],
        "PATCH": [IsAdminUser]
    }

    @extend_schema(
        tags=['Orders'],
        request=UpdateOrderStatusSerializer,
        responses=UPDATE_ORDER_STATUS_RESPONSES
    )
    def patch(self, request, **kwargs):
        _id = kwargs.get("id")
        serializer = UpdateOrderStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        is_done, response_message = update_order_status(order_id=_id, status=serializer.data["status"])
        if not is_done:
            res_status = status.HTTP_406_NOT_ACCEPTABLE
        else:
            res_status = status.HTTP_200_OK
        return Response(data={"message": response_message}, status=res_status)


class SubmitMyOrderAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "PATCH": [IsAuthenticatedAndNotAdmin]
    }

    @extend_schema(
        tags=['Orders'],
        responses=SUBMIT_MY_ORDER_RESPONSES
    )
    def patch(self, request, **kwargs):
        done, message = submit_my_order(user=request.user)
        if not done:
            res_status = status.HTTP_406_NOT_ACCEPTABLE
        else:
            res_status = status.HTTP_200_OK
        return Response(data={"message": message}, status=res_status)


class PaymentsAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "GET": [IsAuthenticated],
        # must be done by payment system API and this is just mock for now
        "POST": [IsAuthenticatedAndNotAdmin]
    }

    @extend_schema(
        tags=['Orders'],
        request=PaymentGenericSerializer,
        description="don't use. this has no real function."
    )
    def post(self, request):
        payment_data = create_payment(data=request.data)
        return Response(data=payment_data, status=status.HTTP_201_CREATED)
