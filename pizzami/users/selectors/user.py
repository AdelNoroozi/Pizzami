from django.db.models import QuerySet, Q

from pizzami.users.models import BaseUser


def get_users(base_only: bool) -> QuerySet:
    if base_only:
        return BaseUser.objects.filter(is_admin=False, is_superuser=False)
    else:
        return BaseUser.objects.all()


def search_users(queryset: QuerySet, search_param: str) -> QuerySet:
    return queryset.filter(Q(email__icontains=search_param) | Q(profile__public_name__icontains=search_param))
