from django.db.models import QuerySet

from pizzami.foods.models import Food


def get_foods() -> QuerySet[Food]:
    return Food.objects.confirmed()
