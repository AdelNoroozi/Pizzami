import uuid

from django.http import QueryDict
from rest_framework.generics import get_object_or_404
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict

from pizzami.ingredients.models import Ingredient
from pizzami.ingredients.selectors import delete_ingredient as delete_ingredient_selector
from pizzami.ingredients.selectors import get_ingredients as get_ingredients_selector
from pizzami.ingredients.serializers import IngredientCompleteOutputSerializer, IngredientBaseOutputSerializer, \
    IngredientInputSerializer
from pizzami.ingredients.filters import IngredientFilter


def get_ingredients(query_dict: QueryDict, is_user_staff: bool) -> ReturnList[Ingredient]:
    queryset = get_ingredients_selector(return_all=is_user_staff)
    filtered_queryset = IngredientFilter(query_dict, queryset=queryset).qs
    if is_user_staff:
        serializer = IngredientCompleteOutputSerializer(filtered_queryset, many=True)
    else:
        serializer = IngredientBaseOutputSerializer(filtered_queryset, many=True)
    return serializer.data


def create_ingredient(data: dict) -> ReturnDict:
    serializer = IngredientInputSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    response_serializer = IngredientCompleteOutputSerializer(serializer.instance, many=False)
    return response_serializer.data


def update_ingredient(ingredient_id: uuid, data: dict) -> ReturnDict:
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    serializer = IngredientInputSerializer(instance=ingredient, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    response_serializer = IngredientCompleteOutputSerializer(serializer.instance, many=False)
    return response_serializer.data


def delete_ingredient(ingredient_id: uuid):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    delete_ingredient_selector(ingredient)
