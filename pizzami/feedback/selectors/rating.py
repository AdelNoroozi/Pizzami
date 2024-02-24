from pizzami.feedback.models import Rating
from pizzami.foods.models import Food
from pizzami.users.models import Profile


def get_or_create_rating(food: Food, user: Profile):
    ratings = Rating.objects.filter(food=food, user=user)
    if ratings.exists():
        return ratings.first()
    return Rating(food=food, user=user)
