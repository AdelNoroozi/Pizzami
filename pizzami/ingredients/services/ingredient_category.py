from pizzami.ingredients.selectors import get_ingredient_categories as get_ingredient_categories_selector
from pizzami.ingredients.serializers.ingredient_category import IngredientCategoryCompleteOutputSerializer, \
    IngredientCategoryBaseOutputSerializer


def get_ingredient_categories(is_user_staff: bool):
    queryset = get_ingredient_categories_selector(is_user_staff)
    if is_user_staff:
        serializer = IngredientCategoryCompleteOutputSerializer(queryset, many=True)
    else:
        serializer = IngredientCategoryBaseOutputSerializer(queryset, many=True)
    return serializer.data
