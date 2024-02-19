from django.utils import timezone

from pizzami.orders.models import Discount


def update_discount_status():
    expired_discounts = Discount.objects.filter(has_time_limit=True, expiration_date__lte=timezone.now())
    expired_discounts.update(is_active=False)
    started_discounts = Discount.objects.filter(has_time_limit=True, start_date__gte=timezone.now())
    started_discounts.update(is_active=True)
