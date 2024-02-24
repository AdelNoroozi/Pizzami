import uuid

from django.db import transaction
from django.http import Http404
from rest_framework.generics import get_object_or_404

from pizzami.feedback.selectors import get_or_create_rating
from pizzami.foods.models import Food
from pizzami.users.models import BaseUser


@transaction.atomic
def create_or_update_rating(food_id: uuid, user: BaseUser, rate: int):
    profile = user.profile
    food = get_object_or_404(Food, id=food_id, is_active=True)
    if (not food.is_public) and (food.created_by != profile):
        raise Http404
    rating = get_or_create_rating(food=food, user=profile)
    if rate == 0:
        rating.delete()
    else:
        rating.rate = rate
        rating.save()
    food.update_rate()
