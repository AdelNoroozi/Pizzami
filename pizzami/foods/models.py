import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg, F
from django.utils.translation import gettext_lazy as _

from pizzami.common.models import ImageIncludedBaseModel, BaseModel
from pizzami.foods.mangers import FoodManager
from pizzami.ingredients.models import IngredientCategory, Ingredient
from pizzami.users.models import Profile


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
        verbose_name_plural = _("Food Category Compounds")
        ordering = ("position",)
        db_table = "food_category_compound"
        indexes = [
            models.Index(fields=["food_category", "position"])
        ]


class Food(ImageIncludedBaseModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=50, verbose_name=_("name"))
    category = models.ForeignKey(FoodCategory, on_delete=models.RESTRICT, related_name="foods",
                                 verbose_name=_("category"))
    created_by = models.ForeignKey(Profile, on_delete=models.RESTRICT, related_name="foods",
                                   verbose_name=_("created by"), blank=True, null=True)
    description = models.TextField(verbose_name=_("description"))
    rate = models.FloatField(
        default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ],
        editable=False,
        verbose_name=_("rate")
    )
    is_original = models.BooleanField(default=True, verbose_name=_("is original"))
    price = models.FloatField(verbose_name=_("price"))
    views = models.PositiveIntegerField(default=0, editable=False, verbose_name=_("views"))
    ordered_count = models.PositiveIntegerField(default=0, editable=False, verbose_name=_("ordered count"))
    is_confirmed = models.BooleanField(default=None, blank=True, null=True, verbose_name=_("is confirmed"))
    is_public = models.BooleanField(default=False, verbose_name=_("is public"))

    objects = FoodManager()

    main_fk_field = "category"

    def __str__(self):
        return f"{self.name}"

    def update_rate(self):
        from pizzami.feedback.models import Rating
        new_rate = Rating.objects.filter(food=self).aggregate(rate_avg=Avg(F("rate")))["rate_avg"]
        self.rate = new_rate
        self.save()

    class Meta:
        verbose_name = _("Food")
        verbose_name_plural = _("Foods")
        ordering = ("position",)
        db_table = "food"
        indexes = [
            models.Index(fields=["category", "position"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["rate"]),
            models.Index(fields=["views"])
        ]


class FoodIngredient(BaseModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name="ingredients", verbose_name=_("food"))
    ingredient = models.ForeignKey(Ingredient, on_delete=models.RESTRICT, related_name="foods",
                                   verbose_name=_("ingredient"))
    amount = models.PositiveIntegerField(verbose_name=_("amount"))

    main_fk_field = "food"

    def __str__(self):
        return f"{self.food.name} - {self.ingredient.name}"

    class Meta:
        verbose_name = _("FoodIngredient")
        verbose_name_plural = _("FoodIngredients")
        ordering = ("position",)
        db_table = "food_ingredient"
        indexes = [
            models.Index(fields=["food", "position"])
        ]
