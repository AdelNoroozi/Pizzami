from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
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
            return Food.objects.confirmed().filter(category__is_active=True)


def search_food(queryset: QuerySet[Food], search_param: str) -> QuerySet[Food]:
    search_vector = SearchVector("name", weight="A") + SearchVector("description", weight="C") + SearchVector(
        "category__name", weight="B")
    search_query = SearchQuery(search_param)
    return queryset.annotate(
        search=search_vector,
        rank=SearchRank(search_vector, search_query)
    ).filter(rank__gte=0.1).order_by("-rank")


def order_foods(queryset: QuerySet[Food], order_param: str) -> QuerySet[Food]:
    return queryset.order_by(order_param)
