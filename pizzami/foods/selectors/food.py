from django.db.models import QuerySet

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
