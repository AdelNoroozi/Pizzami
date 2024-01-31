from django.urls import path

from pizzami.ingredients.apis import IngredientCategoriesAPI, IngredientCategoryAPI, IngredientsAPI, IngredientAPI, \
    IngredientCategoryActivateAPI, IngredientActivateAPI

urlpatterns = [
    path('categories/', IngredientCategoriesAPI.as_view(), name='ingredient_categories'),
    path('categories/<str:id>/', IngredientCategoryAPI.as_view(), name='ingredient_category'),
    path('categories/<str:id>/activate', IngredientCategoryActivateAPI.as_view(),
         name='change_ingredient_category_activation_status'),
    path('', IngredientsAPI.as_view(), name='ingredients'),
    path('<str:id>/', IngredientAPI.as_view(), name='ingredient'),
    path('<str:id>/activate', IngredientActivateAPI.as_view(), name='change_ingredient_activation_status'),
]
