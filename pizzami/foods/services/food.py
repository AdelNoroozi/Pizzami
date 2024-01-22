from rest_framework.utils.serializer_helpers import ReturnList

from pizzami.foods.models import Food
from pizzami.foods.selectors import get_foods as get_foods_selector
from pizzami.foods.serializers import FoodBaseOutputSerializer, FoodDetailedOutputSerializer


def get_foods(is_user_staff: bool) -> ReturnList[Food]:
    queryset = get_foods_selector(return_all=is_user_staff)
    if is_user_staff:
        serializer = FoodDetailedOutputSerializer(queryset, many=True)
    else:
        serializer = FoodBaseOutputSerializer(queryset, many=True)
    return serializer.data
