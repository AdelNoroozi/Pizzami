from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from pizzami.api.mixins import ApiAuthMixin, BasePermissionsMixin
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
    CHANGE_INGREDIENT_CATEGORY_ACTIVATION_STATUS_RESPONSES, CHANGE_INGREDIENT_ACTIVATION_STATUS_RESPONSES
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
        tags=['Ingredients'],
        responses={200: GET_INGREDIENT_CATEGORIES_200_RESPONSE}
    )
    def get(self, request):
        data = get_ingredient_categories(request.user.is_staff)
        return Response(data=data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Ingredients'],
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
        tags=['Ingredients'],
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
        tags=['Ingredients'],
        responses={204: DELETE_INGREDIENT_CATEGORY_204_RESPONSE,
                   401: INGREDIENT_CATEGORY_401_RESPONSE,
                   403: INGREDIENT_CATEGORY_403_RESPONSE,
                   404: INGREDIENT_CATEGORY_404_RESPONSE}
    )
    def delete(self, request, **kwargs):
        _id = kwargs.get("id")
        delete_ingredient_category(ingredient_category_id=_id)
        return Response(data={"message": "done"}, status=status.HTTP_204_NO_CONTENT)


class IngredientCategoryActivateAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "PATCH": [IsAdminUser]
    }

    @extend_schema(
        tags=['Ingredients'],
        description="changes ingredient category's activation status. only for staff users.",
        responses=CHANGE_INGREDIENT_CATEGORY_ACTIVATION_STATUS_RESPONSES)
    def patch(self, request, **kwargs):
        ingredient_category_id = kwargs.get("id")
        new_activation_status = change_activation_status(obj_id=ingredient_category_id, obj_cls=IngredientCategory)
        if new_activation_status:
            activation_str = "activated"
        else:
            activation_str = "deactivated"
        return Response(data={"message": f"ingredient category {activation_str} successfully"})


class IngredientsAPI(ApiAuthMixin, BasePermissionsMixin, APIView):

    @extend_schema(
        tags=['Ingredients'],
        parameters=[OpenApiParameter(name="category")],
        responses={200: GET_INGREDIENTS_200_RESPONSE})
    def get(self, request):
        data = get_ingredients(get_method=request.GET, is_user_staff=request.user.is_staff)
        return Response(data=data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=['Ingredients'],
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
        tags=['Ingredients'],
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
        tags=['Ingredients'],
        responses={204: DELETE_INGREDIENT_204_RESPONSE,
                   401: INGREDIENT_401_RESPONSE,
                   403: INGREDIENT_403_RESPONSE,
                   404: INGREDIENT_404_RESPONSE})
    def delete(self, request, **kwargs):
        _id = kwargs.get("id")
        delete_ingredient(ingredient_id=_id)
        return Response(data={"message": "done"}, status=status.HTTP_204_NO_CONTENT)


class IngredientActivateAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "PATCH": [IsAdminUser]
    }

    @extend_schema(
        tags=['Ingredients'],
        description="changes ingredient's activation status. only for staff users.",
        responses=CHANGE_INGREDIENT_ACTIVATION_STATUS_RESPONSES)
    def patch(self, request, **kwargs):
        ingredient_id = kwargs.get("id")
        new_activation_status = change_activation_status(obj_id=ingredient_id, obj_cls=Ingredient)
        if new_activation_status:
            activation_str = "activated"
        else:
            activation_str = "deactivated"
        return Response(data={"message": f"ingredient {activation_str} successfully"})
