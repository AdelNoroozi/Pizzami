from django.db import models
from django.utils.translation import gettext_lazy as _

from pizzami.common.models import ImageIncludedBaseModel


class FoodCategory(ImageIncludedBaseModel):
    name = models.CharField(max_length=50, verbose_name=_("name"))
    icon_url = models.CharField(max_length=512, verbose_name=_("icon url"))
    icon_alt_text = models.CharField(max_length=50, verbose_name=_("icon alt text"))


class FoodCategoryStructure(models.Model):
    pass


class Food(ImageIncludedBaseModel):
    pass


class FoodIngredient(models.Model):
    pass
