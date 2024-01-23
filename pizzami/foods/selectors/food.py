from django.db.models import QuerySet, Q

from pizzami.foods.models import Food
from pizzami.users.models import Profile


def get_foods(return_all: bool, user_profile: Profile = None) -> QuerySet[Food]:
    if return_all:
        return Food.objects.all()
    else:
        if user_profile:
            return Food.objects.active().filter(created_by=user_profile)
        else:
            return Food.objects.confirmed()


def search_food(queryset: QuerySet[Food], search_param: str) -> QuerySet[Food]:
    return queryset.filter(Q(name__icontains=search_param) | Q(description__icontains=search_param))


def order_foods(queryset: QuerySet[Food], order_param: str) -> QuerySet[Food]:
    return queryset.order_by(order_param)
