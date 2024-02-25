from admin_numeric_filter.admin import SliderNumericFilter, NumericFilterModelAdmin
from django.contrib import admin

from pizzami.common.admin import BaseModelAdmin
from pizzami.ingredients.models import IngredientCategory, Ingredient


@admin.register(IngredientCategory)
class IngredientCategoryAdmin(BaseModelAdmin):
    list_display = ["name"] + BaseModelAdmin.list_display
    search_fields = ["name"]


@admin.register(Ingredient)
class IngredientAdmin(BaseModelAdmin, NumericFilterModelAdmin):
    list_display = ["name", "category", "is_available"] + BaseModelAdmin.list_display + ["remaining_units", "unit",
                                                                                         "price"]
    list_editable = BaseModelAdmin.list_editable + ["remaining_units", "is_available"]
    list_filter = BaseModelAdmin.list_filter + ["category", "is_available", ("price", SliderNumericFilter),
                                                ("remaining_units", SliderNumericFilter)]
    search_fields = ["name", "category__name"]
    ordering = BaseModelAdmin.ordering + ["remaining_units", "price"]
