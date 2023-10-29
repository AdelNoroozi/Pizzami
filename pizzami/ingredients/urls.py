from django.urls import path

from pizzami.ingredients.apis import IngredientCategoriesAPI, IngredientCategoryAPI, IngredientsAPI

urlpatterns = [
    path('categories/', IngredientCategoriesAPI.as_view(), name='ingredient_categories'),
    path('categories/<str:id>/', IngredientCategoryAPI.as_view(), name='ingredient_category'),
    path('', IngredientsAPI.as_view(), name='ingredients'),
]
