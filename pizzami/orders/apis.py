from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from pizzami.api.mixins import ApiAuthMixin, BasePermissionsMixin
from pizzami.orders.documentations import GET_DISCOUNTS_RESPONSES, CREATE_DISCOUNT_RESPONSES, GET_DISCOUNTS_PARAMETERS
from pizzami.orders.serializers import DiscountInputSerializer
from pizzami.orders.services import get_discount_list, create_discount


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
