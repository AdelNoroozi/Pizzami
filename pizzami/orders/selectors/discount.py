from django.contrib.contenttypes.models import ContentType
from django.db.models import QuerySet, Q

from pizzami.orders.models import Discount
from pizzami.users.models import Profile


def get_discount_list(private_only: bool, user: Profile = None) -> QuerySet[Discount]:
    if private_only:
        contenttype_obj = ContentType.objects.get_for_model(user)
        return Discount.objects.active().filter(is_public=False, object_id=user.id, specified_type=contenttype_obj)
    else:
        return Discount.objects.all()


def search_discount(queryset: QuerySet[Discount], search_param: str) -> QuerySet[Discount]:
    return queryset.filter(Q(name__icontains=search_param) | Q(description__icontains=search_param))


def order_discounts(queryset: QuerySet[Discount], order_param: str) -> QuerySet[Discount]:
    return queryset.order_by(order_param)


def specific_filter_discounts(queryset: QuerySet[Discount], object_id: str) -> QuerySet[Discount]:
    return queryset.filter(object_id=object_id)
