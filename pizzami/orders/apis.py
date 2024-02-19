from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from pizzami.api.mixins import ApiAuthMixin, BasePermissionsMixin
from pizzami.orders.documentations import GET_DISCOUNTS_RESPONSES, CREATE_DISCOUNT_RESPONSES, GET_DISCOUNTS_PARAMETERS, \
    DELETE_DISCOUNT_RESPONSES, UPDATE_DISCOUNT_RESPONSES
from pizzami.orders.selectors import has_discount_orders
from pizzami.orders.serializers import DiscountInputSerializer
from pizzami.orders.services import get_discount_list, create_discount, delete_discount, update_discount


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
