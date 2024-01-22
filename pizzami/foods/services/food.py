from rest_framework.utils.serializer_helpers import ReturnList

from pizzami.foods.models import Food
from pizzami.foods.selectors import get_foods as get_foods_selector
from pizzami.foods.serializers import FoodBaseOutputSerializer


def get_foods() -> ReturnList[Food]:
    queryset = get_foods_selector()
    serializer = FoodBaseOutputSerializer(queryset, many=True)
    return serializer.data
