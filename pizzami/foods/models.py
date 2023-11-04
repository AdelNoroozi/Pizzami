import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from pizzami.common.models import ImageIncludedBaseModel, BaseModel
from pizzami.ingredients.models import IngredientCategory


class FoodCategory(ImageIncludedBaseModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=50, verbose_name=_("name"))
    icon_url = models.CharField(max_length=512, verbose_name=_("icon url"))
    icon_alt_text = models.CharField(max_length=50, verbose_name=_("icon alt text"))
    is_customizable = models.BooleanField(verbose_name=_("is customizable"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Food Category")
        verbose_name_plural = _("Food Categories")
        ordering = ("position",)
        db_table = "food_category"


class FoodCategoryCompound(BaseModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    food_category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, related_name="compounds",
                                      verbose_name=_("category"))
    ingredient_category = models.ForeignKey(IngredientCategory, on_delete=models.RESTRICT,
                                            related_name="food_categories", verbose_name=_("ingredient_category"))
    min = models.PositiveIntegerField(default=1, verbose_name=_("min"))
    max = models.PositiveIntegerField(verbose_name=_("max"))

    main_fk_field = "food_category"

    def __str__(self):
        return f"{self.food_category.name} - {self.ingredient_category.name}"

    class Meta:
        verbose_name = _("Food Category Compound")
        verbose_name_plural = _("Food Category Compound")
        ordering = ("position",)
        db_table = "food_category_compound"


class Food(ImageIncludedBaseModel):
    pass


class FoodIngredient(models.Model):
    pass
