from drf_spectacular.utils import extend_schema, OpenApiParameter
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
    FOOD_CATEGORY_404_RESPONSE, DELETE_FOOD_CATEGORY_204_RESPONSE, UPDATE_FOOD_CATEGORY_200_RESPONSE
)
from pizzami.foods.serializers.food_category import FoodCategoryInputSerializer
from pizzami.foods.services import get_food_categories, create_food_category, retrieve_food_category, get_foods
from pizzami.foods.services.food_category import delete_food_category, update_food_category


class FoodCategoriesAPI(ApiAuthMixin, BasePermissionsMixin, APIView):

    @extend_schema(
        parameters=[OpenApiParameter(name="is_customizable")],
        responses={200: GET_FOOD_CATEGORIES_200_RESPONSE}
    )
    def get(self, request):
        data = get_food_categories(get_method=request.GET, is_user_staff=request.user.is_staff)
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

    @extend_schema(
        responses={204: DELETE_FOOD_CATEGORY_204_RESPONSE,
                   401: FOOD_CATEGORY_401_RESPONSE,
                   403: FOOD_CATEGORY_403_RESPONSE,
                   404: FOOD_CATEGORY_404_RESPONSE}

    )
    def delete(self, request, **kwargs):
        _id = kwargs.get("id")
        delete_food_category(food_category_id=_id)
        return Response(data={"message": "done"}, status=status.HTTP_204_NO_CONTENT)

    @extend_schema(request=FoodCategoryInputSerializer,
                   responses={200: UPDATE_FOOD_CATEGORY_200_RESPONSE,
                              400: SAVE_FOOD_CATEGORY_400_RESPONSE,
                              401: FOOD_CATEGORY_401_RESPONSE,
                              403: FOOD_CATEGORY_403_RESPONSE,
                              404: FOOD_CATEGORY_404_RESPONSE})
    def put(self, request, **kwargs):
        _id = kwargs.get("id")
        food_category_data = update_food_category(food_category_id=_id, data=request.data)
        return Response(data=food_category_data, status=status.HTTP_200_OK)


class FoodsAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    def get(self, request):
        get_method = request.GET
        if get_method.get("set") == "mine":
            if (not request.user.is_authenticated) or request.user.is_staff:
                return Response(data={"message": "only authenticated normal users can access their own foods"},
                                status=status.HTTP_403_FORBIDDEN)
            data = get_foods(get_method=get_method, is_user_staff=request.user.is_staff, user_created=True,
                             user=request.user)
        else:
            data = get_foods(get_method=get_method, is_user_staff=request.user.is_staff, user_created=False)
        return Response(data=data, status=status.HTTP_200_OK)
