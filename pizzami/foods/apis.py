from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from pizzami.api.mixins import ApiAuthMixin, BasePermissionsMixin
from pizzami.foods.services import get_food_categories, create_food_category


class FoodCategoriesAPI(ApiAuthMixin, BasePermissionsMixin, APIView):

    def get(self, request):
        data = get_food_categories(is_user_staff=request.user.is_staff)
        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request):
        food_category_data = create_food_category(data=request.data)
        return Response(data=food_category_data, status=status.HTTP_201_CREATED)
