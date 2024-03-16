from django.db import transaction
from django.db.models import RestrictedError
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from pizzami.api.mixins import ApiAuthMixin, BasePermissionsMixin
from pizzami.api.pagination import FullPagination
from pizzami.common.services import change_activation_status
from pizzami.ingredients.documentation import (
    GET_INGREDIENT_CATEGORIES_200_RESPONSE,
    DELETE_INGREDIENT_CATEGORY_204_RESPONSE,
    SAVE_INGREDIENT_CATEGORY_400_RESPONSE,
    CREATE_INGREDIENT_CATEGORY_201_RESPONSE,
    INGREDIENT_CATEGORY_401_RESPONSE,
    INGREDIENT_CATEGORY_403_RESPONSE,
    INGREDIENT_CATEGORY_404_RESPONSE,
    UPDATE_INGREDIENT_CATEGORY_200_RESPONSE,
    GET_INGREDIENTS_200_RESPONSE,
    CREATE_INGREDIENT_201_RESPONSE,
    INGREDIENT_401_RESPONSE,
    INGREDIENT_403_RESPONSE, UPDATE_INGREDIENT_200_RESPONSE, INGREDIENT_404_RESPONSE, DELETE_INGREDIENT_204_RESPONSE,
    CHANGE_INGREDIENT_CATEGORY_ACTIVATION_STATUS_RESPONSES, CHANGE_INGREDIENT_ACTIVATION_STATUS_RESPONSES,
    GET_INGREDIENT_PARAMETERS, DELETE_INGREDIENT_CATEGORY_RESPONSES
)
from pizzami.ingredients.models import IngredientCategory, Ingredient
from pizzami.ingredients.serializers import IngredientCategoryInputSerializer, IngredientInputSerializer
from pizzami.ingredients.services import (
    get_ingredient_categories,
    create_ingredient_category,
    update_ingredient_category,
    delete_ingredient_category,
    get_ingredients,
    create_ingredient, update_ingredient, delete_ingredient
)


class IngredientCategoriesAPI(ApiAuthMixin, BasePermissionsMixin, APIView):

    @extend_schema(
        tags=['Ingredients:Categories'],
        responses={200: GET_INGREDIENT_CATEGORIES_200_RESPONSE}
    )
    def get(self, request):
        data = get_ingredient_categories(request.user.is_staff)
        return Response(data=data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Ingredients:Categories'],
        request=IngredientCategoryInputSerializer,
        responses={201: CREATE_INGREDIENT_CATEGORY_201_RESPONSE,
                   400: SAVE_INGREDIENT_CATEGORY_400_RESPONSE,
                   401: INGREDIENT_CATEGORY_401_RESPONSE,
                   403: INGREDIENT_CATEGORY_403_RESPONSE}
    )
    def post(self, request):
        ingredient_category_data = create_ingredient_category(request.data)
        return Response(data=ingredient_category_data, status=status.HTTP_201_CREATED)


class IngredientCategoryAPI(ApiAuthMixin, BasePermissionsMixin, APIView):

    @extend_schema(
        tags=['Ingredients:Categories'],
        request=IngredientCategoryInputSerializer,
        responses={200: UPDATE_INGREDIENT_CATEGORY_200_RESPONSE,
                   400: SAVE_INGREDIENT_CATEGORY_400_RESPONSE,
                   401: INGREDIENT_CATEGORY_401_RESPONSE,
                   403: INGREDIENT_CATEGORY_403_RESPONSE,
                   404: INGREDIENT_CATEGORY_404_RESPONSE}
    )
    def put(self, request, **kwargs):
        _id = kwargs.get("id")
        updated_ingredient_category_data = update_ingredient_category(ingredient_category_id=_id, data=request.data)
        return Response(data=updated_ingredient_category_data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Ingredients:Categories'],
        responses=DELETE_INGREDIENT_CATEGORY_RESPONSES
    )
    def delete(self, request, **kwargs):
        _id = kwargs.get("id")
        try:
            with transaction.atomic():
                delete_ingredient_category(ingredient_category_id=_id)
        except RestrictedError:
            return Response(data={"message": _(
                "can't delete this category as long as it has ingredients or some food category is using it as one of "
                "its compounds.")},
                status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"message": "done"}, status=status.HTTP_204_NO_CONTENT)


class IngredientCategoryActivateAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "PATCH": [IsAdminUser]
    }

    @extend_schema(
        tags=['Ingredients:Categories'],
        description="changes ingredient category's activation status. only for staff users.",
        responses=CHANGE_INGREDIENT_CATEGORY_ACTIVATION_STATUS_RESPONSES)
    def patch(self, request, **kwargs):
        ingredient_category_id = kwargs.get("id")
        new_activation_status = change_activation_status(obj_id=ingredient_category_id,
                                                         queryset=IngredientCategory.objects.all())
        if new_activation_status:
            activation_str = "activated"
        else:
            activation_str = "deactivated"
        return Response(data={"message": f"ingredient category {activation_str} successfully"})


class IngredientsAPI(ApiAuthMixin, BasePermissionsMixin, APIView):

    @extend_schema(
        tags=['Ingredients:Ingredients'],
        parameters=GET_INGREDIENT_PARAMETERS,
        responses={200: GET_INGREDIENTS_200_RESPONSE})
    def get(self, request):
        data = get_ingredients(query_dict=request.GET, is_user_staff=request.user.is_staff)
        paginator = FullPagination()
        paginated_data = paginator.paginate_queryset(queryset=data, request=request)
        return paginator.get_paginated_response(data={"ok": True, "data": paginated_data, "status": status.HTTP_200_OK})

    @extend_schema(
        tags=['Ingredients:Ingredients'],
        request=IngredientInputSerializer,
        responses={201: CREATE_INGREDIENT_201_RESPONSE,
                   400: SAVE_INGREDIENT_CATEGORY_400_RESPONSE,
                   401: INGREDIENT_401_RESPONSE,
                   403: INGREDIENT_403_RESPONSE})
    def post(self, request):
        ingredient_data = create_ingredient(request.data)
        return Response(data=ingredient_data, status=status.HTTP_201_CREATED)


class IngredientAPI(ApiAuthMixin, BasePermissionsMixin, APIView):

    @extend_schema(
        tags=['Ingredients:Ingredients'],
        request=IngredientInputSerializer,
        responses={200: UPDATE_INGREDIENT_200_RESPONSE,
                   400: SAVE_INGREDIENT_CATEGORY_400_RESPONSE,
                   401: INGREDIENT_401_RESPONSE,
                   403: INGREDIENT_403_RESPONSE,
                   404: INGREDIENT_404_RESPONSE})
    def put(self, request, **kwargs):
        _id = kwargs.get("id")
        updated_ingredient_data = update_ingredient(ingredient_id=_id, data=request.data)
        return Response(data=updated_ingredient_data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Ingredients:Ingredients'],
        responses={204: DELETE_INGREDIENT_204_RESPONSE,
                   401: INGREDIENT_401_RESPONSE,
                   403: INGREDIENT_403_RESPONSE,
                   404: INGREDIENT_404_RESPONSE})
    def delete(self, request, **kwargs):
        _id = kwargs.get("id")
        try:
            with transaction.atomic():
                delete_ingredient(ingredient_id=_id)
        except RestrictedError:
            return Response(data={"message": _("can't delete this ingredient as long as it is used in a food.")},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"message": "done"}, status=status.HTTP_204_NO_CONTENT)


class IngredientActivateAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "PATCH": [IsAdminUser]
    }

    @extend_schema(
        tags=['Ingredients:Ingredients'],
        description="changes ingredient's activation status. only for staff users.",
        responses=CHANGE_INGREDIENT_ACTIVATION_STATUS_RESPONSES)
    def patch(self, request, **kwargs):
        ingredient_id = kwargs.get("id")
        new_activation_status = change_activation_status(obj_id=ingredient_id, queryset=Ingredient.objects.all())
        if new_activation_status:
            activation_str = "activated"
        else:
            activation_str = "deactivated"
        return Response(data={"message": f"ingredient {activation_str} successfully"})
