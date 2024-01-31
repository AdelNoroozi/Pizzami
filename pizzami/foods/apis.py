from django.db import transaction
from django.utils.translation import gettext_lazy as _
from django.db.models import RestrictedError
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from pizzami.api.mixins import ApiAuthMixin, BasePermissionsMixin
from pizzami.common.services import change_activation_status
from pizzami.foods.documentaion import (
    CREATE_FOOD_CATEGORY_201_RESPONSE,
    SAVE_FOOD_CATEGORY_400_RESPONSE,
    FOOD_CATEGORY_401_RESPONSE,
    FOOD_CATEGORY_403_RESPONSE,
    GET_FOOD_CATEGORIES_200_RESPONSE,
    RETRIEVE_FOOD_CATEGORY_200_RESPONSE,
    FOOD_CATEGORY_404_RESPONSE, DELETE_FOOD_CATEGORY_204_RESPONSE, UPDATE_FOOD_CATEGORY_200_RESPONSE,
    GET_FOODS_200_RESPONSE, GET_FOODS_200_PARAMETERS, CREATE_FOOD_RESPONSES, RETRIEVE_FOOD_RESPONSES,
    UPDATE_FOOD_RESPONSES, CHANGE_FOOD_ACTIVATION_STATUS_RESPONSES, CHANGE_FOOD_CATEGORY_ACTIVATION_STATUS_RESPONSES
)
from pizzami.foods.models import Food, FoodCategory
from pizzami.foods.serializers import FoodInputSerializer
from pizzami.foods.serializers.food_category import FoodCategoryInputSerializer
from pizzami.foods.services import get_food_categories, create_food_category, retrieve_food_category, get_foods, \
    create_food, retrieve_food, update_food
from pizzami.foods.services.food_category import delete_food_category, update_food_category


class FoodCategoriesAPI(ApiAuthMixin, BasePermissionsMixin, APIView):

    @extend_schema(
        tags=['Foods'],
        parameters=[OpenApiParameter(name="is_customizable")],
        responses={200: GET_FOOD_CATEGORIES_200_RESPONSE}
    )
    def get(self, request):
        data = get_food_categories(get_method=request.GET, is_user_staff=request.user.is_staff)
        return Response(data=data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Foods'],
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
        tags=['Foods'],
        responses={200: RETRIEVE_FOOD_CATEGORY_200_RESPONSE,
                   404: FOOD_CATEGORY_404_RESPONSE}
    )
    def get(self, request, **kwargs):
        _id = kwargs.get("id")
        food_category_data = retrieve_food_category(food_category_id=_id, is_user_staff=request.user.is_staff)
        return Response(data=food_category_data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Foods'],
        # add 400
        responses={204: DELETE_FOOD_CATEGORY_204_RESPONSE,
                   401: FOOD_CATEGORY_401_RESPONSE,
                   403: FOOD_CATEGORY_403_RESPONSE,
                   404: FOOD_CATEGORY_404_RESPONSE}

    )
    def delete(self, request, **kwargs):
        _id = kwargs.get("id")
        try:
            with transaction.atomic():
                delete_food_category(food_category_id=_id)
        except RestrictedError:
            return Response(data={"message": _("can't delete this category as long as it has foods.")},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"message": "done"}, status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        tags=['Foods'],
        request=FoodCategoryInputSerializer,
        responses={200: UPDATE_FOOD_CATEGORY_200_RESPONSE,
                   400: SAVE_FOOD_CATEGORY_400_RESPONSE,
                   401: FOOD_CATEGORY_401_RESPONSE,
                   403: FOOD_CATEGORY_403_RESPONSE,
                   404: FOOD_CATEGORY_404_RESPONSE})
    def put(self, request, **kwargs):
        _id = kwargs.get("id")
        food_category_data = update_food_category(food_category_id=_id, data=request.data)
        return Response(data=food_category_data, status=status.HTTP_200_OK)


class FoodCategoryActivateAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "PATCH": [IsAdminUser]
    }

    @extend_schema(
        tags=['Foods'],
        description="changes food category's activation status. only for staff users.",
        responses=CHANGE_FOOD_CATEGORY_ACTIVATION_STATUS_RESPONSES)
    def patch(self, request, **kwargs):
        food_category_id = kwargs.get("id")
        new_activation_status = change_activation_status(obj_id=food_category_id, obj_cls=FoodCategory)
        if new_activation_status:
            activation_str = "activated"
        else:
            activation_str = "deactivated"
        return Response(data={"message": f"food category {activation_str} successfully"})


class FoodsAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "GET": [AllowAny],
        "POST": [IsAuthenticated]
    }

    @extend_schema(
        tags=['Foods'],
        parameters=GET_FOODS_200_PARAMETERS,
        responses={200: GET_FOODS_200_RESPONSE}
    )
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

    @extend_schema(
        tags=['Foods'],
        request=FoodInputSerializer,
        responses=CREATE_FOOD_RESPONSES
    )
    def post(self, request):
        food_data = create_food(data=request.data, user=request.user)
        return Response(data=food_data, status=status.HTTP_201_CREATED)


class FoodAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "GET": [AllowAny],
        "PUT": [IsAuthenticated]
    }

    @extend_schema(tags=['Foods'], responses=RETRIEVE_FOOD_RESPONSES)
    def get(self, request, **kwargs):
        _id = kwargs.get("id")
        food_data = retrieve_food(food_id=_id, user=request.user)
        return Response(data=food_data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Foods'],
        description="normal users can only update name, description and publicity of their own foods.",
        request=FoodInputSerializer,
        responses=UPDATE_FOOD_RESPONSES
    )
    def put(self, request, **kwargs):
        _id = kwargs.get("id")
        food_data = update_food(food_id=_id, data=request.data, user=request.user)
        return Response(data=food_data, status=status.HTTP_200_OK)


class FoodActivateAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "PATCH": [IsAdminUser]
    }

    @extend_schema(
        tags=['Foods'],
        description="changes foods activation status. only for staff users.",
        responses=CHANGE_FOOD_ACTIVATION_STATUS_RESPONSES)
    def patch(self, request, **kwargs):
        food_id = kwargs.get("id")
        new_activation_status = change_activation_status(obj_id=food_id, obj_cls=Food)
        if new_activation_status:
            activation_str = "activated"
        else:
            activation_str = "deactivated"
        return Response(data={"message": f"food {activation_str} successfully"})
