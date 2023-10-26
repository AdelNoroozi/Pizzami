import uuid

from rest_framework.generics import get_object_or_404
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict

from pizzami.ingredients.models import IngredientCategory
from pizzami.ingredients.selectors import delete_ingredient_category as delete_ingredient_category_selector
from pizzami.ingredients.selectors import get_ingredient_categories as get_ingredient_categories_selector
from pizzami.ingredients.serializers.ingredient_category import IngredientCategoryCompleteOutputSerializer, \
    IngredientCategoryBaseOutputSerializer, IngredientCategoryInputSerializer


def get_ingredient_categories(is_user_staff: bool) -> ReturnList[IngredientCategory]:
    queryset = get_ingredient_categories_selector(is_user_staff)
    if is_user_staff:
        serializer = IngredientCategoryCompleteOutputSerializer(queryset, many=True)
    else:
        serializer = IngredientCategoryBaseOutputSerializer(queryset, many=True)
    return serializer.data


def create_ingredient_category(data: dict) -> ReturnDict:
    serializer = IngredientCategoryInputSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    response_serializer = IngredientCategoryCompleteOutputSerializer(serializer.instance, many=False)
    return response_serializer.data


def update_ingredient_category(ingredient_category_id: uuid, data: dict) -> ReturnDict:
    ingredient_category = get_object_or_404(IngredientCategory, id=ingredient_category_id)
    serializer = IngredientCategoryInputSerializer(instance=ingredient_category, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    response_serializer = IngredientCategoryCompleteOutputSerializer(serializer.instance, many=False)
    return response_serializer.data


def delete_ingredient_category(ingredient_category_id: uuid) -> None:
    ingredient_category = get_object_or_404(IngredientCategory, id=ingredient_category_id)
    delete_ingredient_category_selector(ingredient_category)
