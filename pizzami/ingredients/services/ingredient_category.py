from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict

from pizzami.ingredients.models import IngredientCategory
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
