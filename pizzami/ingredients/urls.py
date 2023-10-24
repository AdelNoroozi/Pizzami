from django.urls import path

from pizzami.ingredients.apis import IngredientCategoryAPI

urlpatterns = [
    path('categories/', IngredientCategoryAPI.as_view(), name='ingredient_category_list'),
]
