from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict

from pizzami.ingredients.models import Ingredient
from pizzami.ingredients.selectors import get_ingredients as get_ingredients_selector
from pizzami.ingredients.serializers import IngredientCompleteOutputSerializer, IngredientBaseOutputSerializer, \
    IngredientInputSerializer


def get_ingredients(is_user_staff: bool) -> ReturnList[Ingredient]:
    queryset = get_ingredients_selector(return_all=is_user_staff)
    if is_user_staff:
        serializer = IngredientCompleteOutputSerializer(queryset, many=True)
    else:
        serializer = IngredientBaseOutputSerializer(queryset, many=True)
    return serializer.data


def create_ingredient(data: dict) -> ReturnDict:
    serializer = IngredientInputSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    response_serializer = IngredientCompleteOutputSerializer(serializer.instance, many=False)
    return response_serializer.data
