from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from pizzami.api.mixins import ApiAuthMixin, BasePermissionsMixin
from pizzami.orders.documentations import GET_DISCOUNTS_RESPONSES
from pizzami.orders.services import get_discount_list


class DiscountsAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "GET": [IsAuthenticated],
        "POST": [IsAuthenticated]
    }

    @extend_schema(
        tags=['Orders'],
        responses=GET_DISCOUNTS_RESPONSES
    )
    def get(self, request):
        data = get_discount_list(is_user_staff=request.user.is_staff, user=request.user)
        return Response(data=data, status=status.HTTP_200_OK)
