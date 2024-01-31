from django.urls import path

from pizzami.foods.apis import FoodCategoriesAPI, FoodCategoryAPI, FoodsAPI, FoodAPI, FoodActivateAPI

urlpatterns = [
    path('categories/', FoodCategoriesAPI.as_view(), name='food_categories'),
    path('categories/<str:id>', FoodCategoryAPI.as_view(), name='food_category'),
    path('', FoodsAPI.as_view(), name='foods'),
    path('<str:id>', FoodAPI.as_view(), name='food'),
    path('<str:id>/activate', FoodActivateAPI.as_view(), name='change_food_activation_status')
]
