from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from pizzami.api.mixins import ApiAuthMixin, BasePermissionsMixin
from pizzami.foods.services import get_food_categories


class FoodCategoriesAPI(ApiAuthMixin, BasePermissionsMixin, APIView):

    def get(self, request):
        data = get_food_categories(is_user_staff=request.user.is_staff)
        return Response(data=data, status=status.HTTP_200_OK)
