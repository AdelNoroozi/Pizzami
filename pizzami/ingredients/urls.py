from django.urls import path

from pizzami.ingredients.apis import IngredientCategoriesAPI, IngredientCategoryAPI

urlpatterns = [
    path('categories/', IngredientCategoriesAPI.as_view(), name='ingredient_category_list'),
    path('categories/<str:id>/', IngredientCategoryAPI.as_view(), name='ingredient_category_list'),
]
