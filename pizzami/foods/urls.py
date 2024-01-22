from django.urls import path

from pizzami.foods.apis import FoodCategoriesAPI, FoodCategoryAPI, FoodsAPI

urlpatterns = [
    path('categories/', FoodCategoriesAPI.as_view(), name='food_categories'),
    path('categories/<str:id>', FoodCategoryAPI.as_view(), name='food_category'),
    path('', FoodsAPI.as_view(), name='foods')
]
