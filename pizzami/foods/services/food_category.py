import uuid

from django.db import transaction
from rest_framework.generics import get_object_or_404
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict

from pizzami.foods.models import FoodCategory
from pizzami.foods.selectors import delete_food_category as delete_food_category_selector, \
    delete_compounds_by_food_category
from pizzami.foods.selectors import get_food_categories as get_food_categories_selector
from pizzami.foods.serializers import FoodCategoryBaseOutputSerializer
from pizzami.foods.serializers.food_category import FoodCategoryInputSerializer, FoodCategoryCompleteOutputSerializer, \
    FoodCategoryDetailedOutputSerializer
from pizzami.foods.services.food_category_compound import create_food_category_compound


def get_food_categories(is_user_staff: bool) -> ReturnList[FoodCategory]:
    queryset = get_food_categories_selector(return_all=is_user_staff)
    serializer = FoodCategoryBaseOutputSerializer(queryset, many=True)
    return serializer.data


@transaction.atomic
def create_food_category(data: dict) -> ReturnDict:
    serializer = FoodCategoryInputSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    if "compounds" in data:
        compounds = data.pop("compounds")
        for compound_data in compounds:
            create_food_category_compound(food_category=serializer.instance, data=compound_data)
    response_serializer = FoodCategoryCompleteOutputSerializer(serializer.instance, many=False)
    return response_serializer.data


def retrieve_food_category(food_category_id: uuid, is_user_staff: bool) -> ReturnDict:
    food_category = get_object_or_404(FoodCategory, id=food_category_id)
    if is_user_staff:
        serializer = FoodCategoryCompleteOutputSerializer(food_category)
    else:
        serializer = FoodCategoryDetailedOutputSerializer(food_category)
    return serializer.data


def delete_food_category(food_category_id: uuid):
    food_category = get_object_or_404(FoodCategory, id=food_category_id)
    delete_food_category_selector(food_category=food_category)


@transaction.atomic
def update_food_category(food_category_id: uuid, data: dict) -> ReturnDict:
    food_category = get_object_or_404(FoodCategory, id=food_category_id)
    serializer = FoodCategoryInputSerializer(instance=food_category, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    delete_compounds_by_food_category(food_category=food_category)
    if "compounds" in data:
        compounds = data.pop("compounds")
        for compound_data in compounds:
            create_food_category_compound(food_category=serializer.instance, data=compound_data)
    response_serializer = FoodCategoryCompleteOutputSerializer(serializer.instance, many=False)
    return response_serializer.data
