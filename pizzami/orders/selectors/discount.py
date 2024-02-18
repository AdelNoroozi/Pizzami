from django.contrib.contenttypes.models import ContentType
from django.db.models import QuerySet

from pizzami.orders.models import Discount
from pizzami.users.models import Profile


def get_discount_list(private_only: bool, user: Profile = None) -> QuerySet[Discount]:
    if private_only:
        contenttype_obj = ContentType.objects.get_for_model(user)
        return Discount.objects.active().filter(is_public=False, object_id=user.id, specified_type=contenttype_obj)
    else:
        return Discount.objects.all()
