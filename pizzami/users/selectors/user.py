from django.db.models import QuerySet

from pizzami.users.models import BaseUser


def get_users(base_only: bool) -> QuerySet:
    if base_only:
        return BaseUser.objects.filter(is_admin=False, is_superuser=False)
    else:
        return BaseUser.objects.all()
