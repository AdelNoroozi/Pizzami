import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from pizzami.common.models import ImageIncludedBaseModel


class IngredientCategory(ImageIncludedBaseModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=30, verbose_name=_("name"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Ingredient Category")
        verbose_name_plural = _("Ingredient Categories")
        ordering = ("position",)
        db_table = "ingredient_category"


class Ingredient(ImageIncludedBaseModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    category = models.ForeignKey(IngredientCategory, on_delete=models.RESTRICT, related_name="ingredients",
                                 verbose_name=_("category"))
    name = models.CharField(max_length=30, verbose_name=_("name"))
    png_file_url = models.CharField(max_length=512, verbose_name=_("png file url"))
    png_file_alt_text = models.CharField(max_length=50, verbose_name=_("png file alt text"))
    price = models.FloatField(verbose_name=_("price"))
    unit = models.CharField(max_length=30, verbose_name=_("unit"))
    remaining_units = models.PositiveIntegerField(default=0, verbose_name=_("remaining units"))
    stock_limit = models.PositiveIntegerField(blank=True, null=True, verbose_name=_("stock limit"))
    is_available = models.BooleanField(default=True, verbose_name=_("is available"))
    auto_check_availability = models.BooleanField(default=False, verbose_name=_("auto check availability"))

    main_fk_field = "category"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.auto_check_availability:
            if self.stock_limit and self.stock_limit >= self.remaining_units:
                self.is_available = False
        super(Ingredient, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Ingredient")
        verbose_name_plural = _("Ingredients")
        ordering = ("position",)
        db_table = "ingredient"
        indexes = [
            models.Index(fields=["category", "position"])
        ]
