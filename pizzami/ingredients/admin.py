from django.contrib import admin

from pizzami.ingredients.models import IngredientCategory, Ingredient

admin.site.register(IngredientCategory)
admin.site.register(Ingredient)
