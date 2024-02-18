from rest_framework.utils.serializer_helpers import ReturnList

from pizzami.orders.models import Discount
from pizzami.orders.serializers import DiscountBaseOutputSerializer
from pizzami.users.models import BaseUser
from pizzami.orders.selectors import get_discount_list as get_discount_list_selector


def get_discount_list(is_user_staff: bool, user: BaseUser = None) -> ReturnList[Discount]:
    if is_user_staff:
        pass
    else:
        queryset = get_discount_list_selector(private_only=True, user=user.profile)
        serializer = DiscountBaseOutputSerializer(queryset, many=True)
        return serializer.data
