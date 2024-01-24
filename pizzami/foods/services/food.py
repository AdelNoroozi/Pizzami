from django.db import transaction
from django.http import QueryDict
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict

from pizzami.foods.filters import FoodFilter
from pizzami.foods.models import Food
from pizzami.foods.selectors import get_foods as get_foods_selector, search_food, order_foods
from pizzami.foods.serializers import FoodBaseOutputSerializer, FoodDetailedOutputSerializer, FoodInputSerializer, \
    FoodCompleteOutputSerializer
from pizzami.foods.services import create_food_ingredient
from pizzami.users.models import BaseUser


def get_foods(get_method: QueryDict, is_user_staff: bool, user_created: bool, user: BaseUser = None) -> ReturnList[
    Food]:
    if user_created:
        queryset = get_foods_selector(return_all=False, user_profile=user.profile)
    else:
        queryset = get_foods_selector(return_all=is_user_staff)
    search_param = get_method.get('search')
    order_param = get_method.get('order_by')
    if search_param:
        queryset = search_food(queryset=queryset, search_param=search_param)
    queryset = FoodFilter(get_method, queryset=queryset).qs
    if order_param and \
            order_param.lstrip("-") in ["rate", "price", "ordered_count", "position", "created_at", "modified_at"]:
        queryset = order_foods(queryset=queryset, order_param=order_param)
    if is_user_staff or user_created:
        serializer = FoodDetailedOutputSerializer(queryset, many=True)
    else:
        serializer = FoodBaseOutputSerializer(queryset, many=True)
    return serializer.data


@transaction.atomic
def create_food(data: dict, user: BaseUser) -> ReturnDict:
    serializer = FoodInputSerializer(data=data, context={"user": user})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    if "ingredients" in data:
        ingredients = data.pop("ingredients")
        for ingredient_data in ingredients:
            create_food_ingredient(food=serializer.instance, data=ingredient_data)
    response_serializer = FoodCompleteOutputSerializer(serializer.instance, many=False)
    return response_serializer.data
