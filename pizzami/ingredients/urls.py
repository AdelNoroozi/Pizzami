from django.urls import path

from pizzami.ingredients.apis import IngredientCategoriesAPI

urlpatterns = [
    path('categories/', IngredientCategoriesAPI.as_view(), name='ingredient_category_list'),
]
