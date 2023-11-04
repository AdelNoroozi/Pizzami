from django.contrib import admin

from pizzami.ingredients.models import IngredientCategory, Ingredient


@admin.register(IngredientCategory)
class IngredientCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "position"]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "position"]
