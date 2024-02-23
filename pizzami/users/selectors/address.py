from django.db.models import QuerySet, Q

from pizzami.users.models import Profile, Address


def get_addresses_by_user(user: Profile) -> QuerySet[Address]:
    return Address.objects.active().filter(user=user)


def search_address(queryset: QuerySet[Address], search_param: str) -> QuerySet[Address]:
    return queryset.filter(Q(title__icontains=search_param) | Q(address_str__icontains=search_param)).distinct()
