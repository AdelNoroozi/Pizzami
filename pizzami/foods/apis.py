from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from pizzami.api.mixins import ApiAuthMixin, BasePermissionsMixin
from pizzami.foods.documentaion import (
    CREATE_FOOD_CATEGORY_201_RESPONSE,
    SAVE_FOOD_CATEGORY_400_RESPONSE,
    FOOD_CATEGORY_401_RESPONSE,
    FOOD_CATEGORY_403_RESPONSE,
    GET_FOOD_CATEGORIES_200_RESPONSE,
RETRIEVE_FOOD_CATEGORY_200_RESPONSE,
FOOD_CATEGORY_404_RESPONSE
)
from pizzami.foods.serializers.food_category import FoodCategoryInputSerializer
from pizzami.foods.services import get_food_categories, create_food_category, retrieve_food_category


class FoodCategoriesAPI(ApiAuthMixin, BasePermissionsMixin, APIView):

    @extend_schema(
        responses={200: GET_FOOD_CATEGORIES_200_RESPONSE}
    )
    def get(self, request):
        data = get_food_categories(is_user_staff=request.user.is_staff)
        return Response(data=data, status=status.HTTP_200_OK)

    @extend_schema(
        request=FoodCategoryInputSerializer,
        responses={201: CREATE_FOOD_CATEGORY_201_RESPONSE,
                   400: SAVE_FOOD_CATEGORY_400_RESPONSE,
                   401: FOOD_CATEGORY_401_RESPONSE,
                   403: FOOD_CATEGORY_403_RESPONSE}
    )
    def post(self, request):
        food_category_data = create_food_category(data=request.data)
        return Response(data=food_category_data, status=status.HTTP_201_CREATED)


class FoodCategoryAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    @extend_schema(
        responses={200: RETRIEVE_FOOD_CATEGORY_200_RESPONSE,
                   404: FOOD_CATEGORY_404_RESPONSE}
    )
    def get(self, request, **kwargs):
        _id = kwargs.get("id")
        food_category_data = retrieve_food_category(food_category_id=_id, is_user_staff=request.user.is_staff)
        return Response(data=food_category_data, status=status.HTTP_200_OK)
