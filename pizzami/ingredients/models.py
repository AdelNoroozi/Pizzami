import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from pizzami.common.models import ImageIncludedBaseModel


class IngredientCategory(ImageIncludedBaseModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4())
    name = models.CharField(max_length=30, verbose_name=_("name"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Ingredient Category")
        verbose_name_plural = _("Ingredient Categories")
        db_table = "ingredient_category"


class Ingredient(ImageIncludedBaseModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4())
    category = models.ForeignKey(IngredientCategory, on_delete=models.CASCADE, related_name="ingredients",
                                 verbose_name=_("category"))
    name = models.CharField(max_length=30, verbose_name=_("name"))
    png_file_url = models.CharField(max_length=512, verbose_name=_("png file url"))
    png_file_alt_text = models.CharField(max_length=50, verbose_name=_("png file alt text"))
    price = models.FloatField(verbose_name=_("price"))
    unit = models.CharField(max_length=30, verbose_name=_("unit"))
    remaining_units = models.PositiveIntegerField(default=0, verbose_name=_("remaining units"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        db_table = "ingredient"
