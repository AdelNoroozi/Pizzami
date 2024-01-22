from rest_framework.utils.serializer_helpers import ReturnList

from pizzami.foods.models import Food
from pizzami.foods.selectors import get_foods as get_foods_selector
from pizzami.foods.serializers import FoodBaseOutputSerializer, FoodDetailedOutputSerializer
from pizzami.users.models import BaseUser


def get_foods(is_user_staff: bool, user_created: bool, user: BaseUser = None) -> ReturnList[Food]:
    if user_created:
        queryset = get_foods_selector(return_all=False, user_profile=user.profile)
    else:
        queryset = get_foods_selector(return_all=is_user_staff)
    if is_user_staff or user_created:
        serializer = FoodDetailedOutputSerializer(queryset, many=True)

    else:
        serializer = FoodBaseOutputSerializer(queryset, many=True)
    return serializer.data
