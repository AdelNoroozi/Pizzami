from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
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
            return Food.objects.confirmed().filter(category__is_active=True)


def search_food(queryset: QuerySet[Food], search_param: str) -> QuerySet[Food]:
    trigram_similarity = TrigramSimilarity("name", search_param) + \
                         TrigramSimilarity("description", search_param) + \
                         TrigramSimilarity("category__name", search_param)
    search_vector = SearchVector("name", weight="A") + SearchVector("description", weight="C") + SearchVector(
        "category__name", weight="B")
    search_query = SearchQuery(search_param)
    return queryset.annotate(
        search=search_vector,
        rank=SearchRank(search_vector, search_query),
        trigram_similarity=trigram_similarity
    ).filter(Q(trigram_similarity__gte=0.3) | Q(rank__gte=0.1)).distinct().order_by("-trigram_similarity", "-rank")


def order_foods(queryset: QuerySet[Food], order_param: str) -> QuerySet[Food]:
    return queryset.order_by(order_param)


def add_food_tags(food: Food, tags: list[str]):
    food.tags.all().delete()
    food.tags.add(*tags, food.name, food.category.name)
