from django.urls import path

from pizzami.foods.apis import FoodCategoriesAPI

urlpatterns = [
    path('categories/', FoodCategoriesAPI.as_view(), name='food_categories')
]
