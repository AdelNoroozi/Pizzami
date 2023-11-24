from django.contrib import admin

from pizzami.common.admin import BaseModelAdmin
from pizzami.foods.models import FoodCategory, FoodCategoryCompound


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
