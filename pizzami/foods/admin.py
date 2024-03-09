from admin_numeric_filter.admin import SliderNumericFilter, NumericFilterModelAdmin
from django.contrib import admin

from pizzami.common.admin import BaseModelAdmin
from pizzami.foods.models import FoodCategory, FoodCategoryCompound, FoodIngredient, Food


class FoodCategoryCompoundInlineAdmin(admin.TabularInline):
    model = FoodCategoryCompound


@admin.register(FoodCategory)
class FoodCategoryAdmin(BaseModelAdmin):
    inlines = (FoodCategoryCompoundInlineAdmin,)
    list_display = ["name"] + BaseModelAdmin.list_display
    list_filter = BaseModelAdmin.list_filter + ["is_customizable"]
    search_fields = ["name"]
    prepopulated_fields = {
        "image_alt_text": ("name",),
        "icon_alt_text": ("name",),
    }


class FoodIngredientInlineAdmin(admin.TabularInline):
    model = FoodIngredient


@admin.register(Food)
class FoodAdmin(BaseModelAdmin,  NumericFilterModelAdmin):
    inlines = (FoodIngredientInlineAdmin,)
    list_display = ["name", "price"] + BaseModelAdmin.list_display + ["rate", "is_confirmed", "is_public",
                                                                      "is_available", "auto_check_availability", "rate",
                                                                      "views", "ordered_count", "is_original"]
    list_editable = BaseModelAdmin.list_editable + ["is_confirmed", "is_public", "is_available",
                                                    "auto_check_availability"]
    list_filter = BaseModelAdmin.list_filter + ["is_public", "is_confirmed", "is_original", "is_available",
                                                "tags__name",
                                                ("price", SliderNumericFilter),
                                                ("ordered_count", SliderNumericFilter)]
    search_fields = ["name", "description", "tags__name"]
    prepopulated_fields = {
        "image_alt_text": ("name",),
    }
    ordering = BaseModelAdmin.ordering + ["rate", "views"]
