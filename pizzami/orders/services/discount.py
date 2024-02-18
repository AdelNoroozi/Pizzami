from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict

from pizzami.orders.models import Discount
from pizzami.orders.selectors import get_discount_list as get_discount_list_selector
from pizzami.orders.serializers import DiscountBaseOutputSerializer, DiscountCompleteOutputSerializer, \
    DiscountInputSerializer
from pizzami.users.models import BaseUser


def get_discount_list(is_user_staff: bool, user: BaseUser = None) -> ReturnList[Discount]:
    if is_user_staff:
        queryset = get_discount_list_selector(private_only=False)
        serializer = DiscountCompleteOutputSerializer(queryset, many=True)
    else:
        queryset = get_discount_list_selector(private_only=True, user=user.profile)
        serializer = DiscountBaseOutputSerializer(queryset, many=True)
    return serializer.data


def create_discount(data: dict) -> ReturnDict:
    serializer = DiscountInputSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    response_serializer = DiscountCompleteOutputSerializer(serializer.instance, many=False)
    return response_serializer.data
