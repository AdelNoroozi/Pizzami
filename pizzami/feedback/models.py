import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from pizzami.common.models import TimeStampedBaseModel
from pizzami.foods.models import Food
from pizzami.users.models import Profile


class Rating(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name="ratings", verbose_name=_("food"))
    user = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name="ratings", verbose_name=_("user"))
    rate = models.PositiveIntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ],
        verbose_name=_("rate"))

    def __str__(self):
        return f"'{self.user.public_name}' for '{self.food.name}'"

    class Meta:
        verbose_name = _("Rating")
        verbose_name_plural = _("Ratings")
        db_table = "rating"
        unique_together = ("user", "food")
        indexes = [
            models.Index(fields=["food"])
        ]


class Comment(MPTTModel, TimeStampedBaseModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name="comments", verbose_name=_("food"))
    user = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name="comments", verbose_name=_("user"))
    parent = TreeForeignKey("self", on_delete=models.CASCADE, related_name="children", blank=True, null=True,
                            verbose_name=_("parent"))
    text = models.TextField(verbose_name=_("text"))
    is_confirmed = models.BooleanField(blank=True, null=True, default=None, verbose_name=_("is confirmed"))

    main_fk_field = "parent"

    def __str__(self):
        return f"'{self.user.public_name}' for '{self.food.name}' on {self.created_at}"

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        db_table = "comment"
        ordering = ("position",)
        indexes = [
            models.Index(fields=["food", "position"]),
            models.Index(fields=["user", "position"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["updated_at"])
        ]
