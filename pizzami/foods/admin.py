from django.contrib import admin

from pizzami.foods.models import FoodCategory, FoodCategoryCompound


class FoodCategoryCompoundInlineAdmin(admin.TabularInline):
    model = FoodCategoryCompound


@admin.register(FoodCategory)
class FoodCategoryAdmin(admin.ModelAdmin):
    inlines = (FoodCategoryCompoundInlineAdmin,)
