import uuid
from typing import Union

from django.db import transaction
from django.http import QueryDict, Http404
from rest_framework.generics import get_object_or_404
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict

from pizzami.foods.filters import FoodFilter
from pizzami.foods.models import Food
from pizzami.foods.selectors import get_foods as get_foods_selector, search_food, order_foods, \
    delete_food_ingredients_by_food, add_food_tags
from pizzami.foods.serializers import FoodBaseOutputSerializer, FoodDetailedOutputSerializer, FoodInputSerializer, \
    FoodCompleteOutputSerializer, FoodPublicDetailedOutputSerializer, FoodMinorInputSerializer
from pizzami.foods.services.food_ingredient import create_food_ingredient
from pizzami.users.models import BaseUser


def get_foods(query_dict: QueryDict, is_user_staff: bool, user_created: bool, user: BaseUser = None) -> ReturnList[
    Food]:
    if user_created:
        queryset = get_foods_selector(return_all=False, user_profile=user.profile)
    else:
        queryset = get_foods_selector(return_all=is_user_staff)
    search_param = query_dict.get('search')
    order_param = query_dict.get('order_by')
    if search_param:
        queryset = search_food(queryset=queryset, search_param=search_param)
    queryset = FoodFilter(query_dict, queryset=queryset).qs
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
    if "tags" in data:
        add_food_tags(food=serializer.instance, tags=data.pop("tags"))
    response_serializer = FoodCompleteOutputSerializer(serializer.instance, many=False)
    return response_serializer.data


@transaction.atomic
def retrieve_food(food_id: uuid, user: BaseUser = None) -> ReturnDict:
    food = get_object_or_404(Food, id=food_id)
    if user.is_authenticated and (user.is_staff or food.created_by == user.profile):
        serializer = FoodCompleteOutputSerializer(food)
    else:
        if not food.is_confirmed:
            raise Http404()
        food.views += 1
        food.save()
        serializer = FoodPublicDetailedOutputSerializer(food)
    return serializer.data


@transaction.atomic
def update_food(food_id: uuid, data: dict, user: BaseUser):
    if not user.is_staff:
        food = get_object_or_404(Food, id=food_id, created_by=user.profile)
        serializer = FoodMinorInputSerializer(instance=food, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        food.is_confirmed = None
        food.save()
    else:
        food = get_object_or_404(Food, id=food_id)
        serializer = FoodInputSerializer(instance=food, data=data, partial=True, context={"user": user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        delete_food_ingredients_by_food(food=food)
        if "ingredients" in data:
            ingredients = data.pop("ingredients")
            for ingredient_data in ingredients:
                create_food_ingredient(food=serializer.instance, data=ingredient_data)
    add_food_tags(food=serializer.instance, tags=data.pop("tags"))
    response_serializer = FoodCompleteOutputSerializer(serializer.instance, many=False)
    return response_serializer.data


def confirm_food(food_id: uuid, action: str) -> Union[None, bool]:
    valid_actions = ["confirm", "reject", "suspend"]

    if action not in valid_actions:
        return False

    food = get_object_or_404(Food, id=food_id)

    if action == "confirm":
        if food.is_confirmed is not True:
            food.is_confirmed = True
            food.save()
            return True
    elif action == "reject":
        if food.is_confirmed is not False:
            food.is_confirmed = False
            food.is_public = False
            food.save()
            return True
    elif action == "suspend":
        if food.is_confirmed is not None:
            food.is_confirmed = None
            food.save()
            return True

    return None


def add_food_ordered_count(food: Food, count: int):
    food.ordered_count = food.ordered_count + count
    food.save()
