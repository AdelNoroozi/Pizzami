import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from pizzami.common.models import TimeStampedBaseModel
from pizzami.foods.models import Food
from pizzami.users.models import Profile


class Discount(TimeStampedBaseModel):
    TYPE_ABSOLUTE = "ABS"
    TYPE_RATIO = "RAT"

    TYPE_CHOICES = (
        (TYPE_ABSOLUTE, "absolute"),
        (TYPE_RATIO, "ration")
    )

    SPECIFIED_TO_USER = "USR"
    SPECIFIED_TO_FOOD = "FOD"
    SPECIFIED_TO_CATEGORY = "CAT"

    SPECIFIED_TO_CHOICES = (
        (SPECIFIED_TO_USER, "user"),
        (SPECIFIED_TO_FOOD, "food"),
        (SPECIFIED_TO_CATEGORY, "category")
    )

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=50, verbose_name=_("name"))
    description = models.TextField(blank=True, null=True, verbose_name=_("description"))
    is_public = models.BooleanField(default=True, verbose_name=_("is public"))
    code = models.CharField(max_length=10, unique=True, null=True, verbose_name=_("code"))
    has_time_limit = models.BooleanField(default=False, verbose_name=_("has time limit"))
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name=_("type"))
    start_date = models.DateTimeField(blank=True, null=True, verbose_name=_("start date"))
    expiration_date = models.DateTimeField(blank=True, null=True, verbose_name=_("expiration date"))
    specified_to_type = models.CharField(max_length=20, blank=True, null=True, choices=SPECIFIED_TO_CHOICES,
                                         verbose_name=_("specified to type"))
    specified_object = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="discounts",
                                         verbose_name=_("specified object"))
    object_id = models.CharField(max_length=50)
    content_object = GenericForeignKey('specified_object', 'object_id')
    percentage_value = models.FloatField(
        blank=True, null=True,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ],
        verbose_name=_("percentage value")
    )
    absolute_value = models.FloatField(blank=True, null=True, verbose_name=_("absolute value"))

    def __str__(self):
        return self.name

    def clean(self) -> None:
        super().clean()

        if self.has_time_limit and (self.start_date is None or self.expiration_date is None):
            raise ValidationError(_("time limited discounts must have start and expiration date"))

        if self.type == self.TYPE_ABSOLUTE and self.absolute_value is None:
            raise ValidationError(_("absolute discounts must have a absolute value"))

        if self.type == self.TYPE_RATIO and self.percentage_value is None:
            raise ValidationError(_("ratio discounts must have a percentage value"))

    class Meta:
        verbose_name = _("Discount")
        verbose_name_plural = _("Discounts")
        ordering = ("position",)
        db_table = "discount"


class Cart(TimeStampedBaseModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(Profile, on_delete=models.RESTRICT, related_name="carts", verbose_name=_("user"))


class CartItem(TimeStampedBaseModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    food = models.ForeignKey(Food, on_delete=models.RESTRICT, related_name="cart_items", verbose_name=_("food"))
    count = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name=_("count"))
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items", verbose_name=_("cart"))