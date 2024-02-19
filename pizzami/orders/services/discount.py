from django.http import QueryDict
from rest_framework.generics import get_object_or_404
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict

from pizzami.orders.filters import DiscountFilter
from pizzami.orders.models import Discount
from pizzami.orders.selectors import get_discount_list as get_discount_list_selector, order_discounts, search_discount, \
    specific_filter_discounts, delete_discount as delete_discount_selector
from pizzami.orders.serializers import DiscountBaseOutputSerializer, DiscountCompleteOutputSerializer, \
    DiscountInputSerializer
from pizzami.users.models import BaseUser


def get_discount_list(query_dict: QueryDict, is_user_staff: bool, user: BaseUser = None) -> ReturnList[Discount]:
    if is_user_staff:
        queryset = get_discount_list_selector(private_only=False)
        search_param = query_dict.get('search')
        order_param = query_dict.get('order_by')
        specified_to = query_dict.get('specified_to')
        if search_param:
            queryset = search_discount(queryset=queryset, search_param=search_param)
        queryset = DiscountFilter(query_dict, queryset=queryset).qs
        if specified_to:
            queryset = specific_filter_discounts(queryset=queryset, object_id=specified_to)
        if order_param and \
                order_param.lstrip("-") in ["start_date", "expiration_date", "position", "created_at", "modified_at",
                                            "absolute_value", "percentage_value"]:
            queryset = order_discounts(queryset=queryset, order_param=order_param)
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


def delete_discount(discount_id: str):
    discount = get_object_or_404(Discount, id=discount_id)
    delete_discount_selector(discount=discount)


def update_discount(discount_id: str, data: dict) -> ReturnDict:
    discount = get_object_or_404(Discount, id=discount_id)
    serializer = DiscountInputSerializer(instance=discount, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    response_serializer = DiscountCompleteOutputSerializer(serializer.instance, many=False)
    return response_serializer.data
