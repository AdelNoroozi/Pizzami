from django.db.models import QuerySet

from pizzami.orders.models import Discount
from pizzami.users.models import Profile


def get_discount_list(private_only: bool, user: Profile = None) -> QuerySet[Discount]:
    if private_only:
        return Discount.objects.active().filter(is_public=False, specified_object=user)
    else:
        return Discount.objects.all()
