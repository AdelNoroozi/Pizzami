from django.contrib.contenttypes.models import ContentType
from django.db.models import QuerySet, Q

from pizzami.orders.models import Discount, Order
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


def deactivate_discounts_by_obj(object_id: str):
    Discount.objects.filter(object_id=object_id).update(is_active=False)


def get_discount_by_food_or_category(food_id: str, category_id: str) -> Discount | None:
    if Discount.objects.filter(is_active=True, is_public=True, object_id=food_id).exists():
        return Discount.objects.filter(is_active=True, is_public=True, object_id=food_id).first()
    elif Discount.objects.filter(is_active=True, is_public=True, object_id=category_id).exists():
        return Discount.objects.filter(is_active=True, is_public=True, object_id=category_id).first()
    else:
        return None


def has_discount_orders(discount_id: str) -> bool:
    if Order.objects.filter(discount__id=discount_id).exists():
        return True
    else:
        return False


def delete_discount(discount: Discount):
    discount.delete()


def inquiry_discount_by_code(code: str, user: Profile) -> str | None:
    discounts = Discount.objects.active().filter(code=code)
    if discounts.exists():
        discount = discounts.first()
        if discount.is_public or (
                discount.specified_to_type == Discount.SPECIFIED_TO_USER and discount.object_id == user.id):
            return discount.id
    return None
