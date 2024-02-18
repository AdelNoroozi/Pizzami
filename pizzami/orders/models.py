import uuid

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from pizzami.common.models import TimeStampedBaseModel
from pizzami.foods.models import Food
from pizzami.users.models import Profile


class Cart(TimeStampedBaseModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(Profile, on_delete=models.RESTRICT, related_name="carts", verbose_name=_("user"))


class CartItem(TimeStampedBaseModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    food = models.ForeignKey(Food, on_delete=models.RESTRICT, related_name="cart_items", verbose_name=_("food"))
    count = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name=_("count"))
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items", verbose_name=_("cart"))
