from rest_framework.utils.serializer_helpers import ReturnList

from pizzami.foods.models import FoodCategory
from pizzami.foods.selectors import get_food_categories as get_food_categories_selector
from pizzami.foods.serializers import FoodCategoryBaseOutputSerializer


def get_food_categories(is_user_staff: bool) -> ReturnList[FoodCategory]:
    queryset = get_food_categories_selector(return_all=is_user_staff)
    serializer = FoodCategoryBaseOutputSerializer(queryset, many=True)
    return serializer.data
