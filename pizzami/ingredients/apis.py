from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from pizzami.api.mixins import ApiAuthMixin, BasePermissionsMixin
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
    INGREDIENT_403_RESPONSE, UPDATE_INGREDIENT_200_RESPONSE, INGREDIENT_404_RESPONSE
)
from pizzami.ingredients.serializers import IngredientCategoryInputSerializer, IngredientInputSerializer
from pizzami.ingredients.services import (
    get_ingredient_categories,
    create_ingredient_category,
    update_ingredient_category,
    delete_ingredient_category,
    get_ingredients,
    create_ingredient, update_ingredient
)


class IngredientCategoriesAPI(ApiAuthMixin, BasePermissionsMixin, APIView):

    @extend_schema(
        responses={200: GET_INGREDIENT_CATEGORIES_200_RESPONSE}
    )
    def get(self, request):
        data = get_ingredient_categories(request.user.is_staff)
        return Response(data=data, status=status.HTTP_200_OK)

    @extend_schema(
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
        responses={204: DELETE_INGREDIENT_CATEGORY_204_RESPONSE,
                   401: INGREDIENT_CATEGORY_401_RESPONSE,
                   403: INGREDIENT_CATEGORY_403_RESPONSE,
                   404: INGREDIENT_CATEGORY_404_RESPONSE}
    )
    def delete(self, request, **kwargs):
        _id = kwargs.get("id")
        delete_ingredient_category(ingredient_category_id=_id)
        return Response(data={"message": "done"}, status=status.HTTP_204_NO_CONTENT)


class IngredientsAPI(ApiAuthMixin, BasePermissionsMixin, APIView):

    @extend_schema(
        responses={200: GET_INGREDIENTS_200_RESPONSE}
    )
    def get(self, request):
        data = get_ingredients(is_user_staff=request.user.is_staff)
        return Response(data=data, status=status.HTTP_200_OK)

    @extend_schema(request=IngredientInputSerializer,
                   responses={201: CREATE_INGREDIENT_201_RESPONSE,
                              400: SAVE_INGREDIENT_CATEGORY_400_RESPONSE,
                              401: INGREDIENT_401_RESPONSE,
                              403: INGREDIENT_403_RESPONSE})
    def post(self, request):
        ingredient_data = create_ingredient(request.data)
        return Response(data=ingredient_data, status=status.HTTP_201_CREATED)


class IngredientAPI(ApiAuthMixin, BasePermissionsMixin, APIView):

    @extend_schema(request=IngredientInputSerializer,
                   responses={200: UPDATE_INGREDIENT_200_RESPONSE,
                              400: SAVE_INGREDIENT_CATEGORY_400_RESPONSE,
                              401: INGREDIENT_401_RESPONSE,
                              403: INGREDIENT_403_RESPONSE,
                              404: INGREDIENT_404_RESPONSE})
    def put(self, request, **kwargs):
        _id = kwargs.get("id")
        updated_ingredient_data = update_ingredient(ingredient_id=_id, data=request.data)
        return Response(data=updated_ingredient_data, status=status.HTTP_200_OK)
