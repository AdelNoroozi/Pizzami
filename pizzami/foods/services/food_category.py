from django.db import transaction
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict

from pizzami.foods.models import FoodCategory
from pizzami.foods.selectors import get_food_categories as get_food_categories_selector
from pizzami.foods.serializers import FoodCategoryBaseOutputSerializer
from pizzami.foods.serializers.food_category import FoodCategoryInputSerializer, FoodCategoryCompleteOutputSerializer
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
