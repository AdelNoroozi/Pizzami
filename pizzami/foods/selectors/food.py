from django.db.models import QuerySet

from pizzami.foods.models import Food


def get_foods(return_all: bool) -> QuerySet[Food]:
    if return_all:
        return Food.objects.all()
    else:
        return Food.objects.confirmed()
