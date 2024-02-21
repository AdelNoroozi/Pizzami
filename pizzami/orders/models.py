import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import F, Sum
from django.utils.translation import gettext_lazy as _

from pizzami.common.models import TimeStampedBaseModel
from pizzami.foods.models import Food
from pizzami.users.models import Profile


class Discount(TimeStampedBaseModel):
    TYPE_ABSOLUTE = "ABS"
    TYPE_RATIO = "RAT"

    TYPE_CHOICES = (
        (TYPE_ABSOLUTE, "absolute"),
        (TYPE_RATIO, "ratio")
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
    code = models.CharField(max_length=10, unique=True, blank=True, null=True, verbose_name=_("code"))
    has_time_limit = models.BooleanField(default=False, verbose_name=_("has time limit"))
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name=_("type"))
    start_date = models.DateTimeField(blank=True, null=True, verbose_name=_("start date"))
    expiration_date = models.DateTimeField(blank=True, null=True, verbose_name=_("expiration date"))
    specified_to_type = models.CharField(max_length=20, blank=True, null=True, choices=SPECIFIED_TO_CHOICES,
                                         verbose_name=_("specified to type"))
    specified_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="discounts",
                                       blank=True, null=True, verbose_name=_("specified type"))
    object_id = models.CharField(max_length=50, blank=True, null=True)
    specified_object = GenericForeignKey('specified_type', 'object_id')
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

        if self.specified_to_type == self.SPECIFIED_TO_USER or self.specified_to_type is None:
            if not self.code:
                raise ValidationError(_("User-specified or public broad discounts must have a code."))
        else:
            if self.code:
                raise ValidationError(_("Food or food category specified discounts must not have a code."))

        if self.specified_to_type == self.SPECIFIED_TO_USER and self.is_public:
            raise ValidationError(_("user specified discounts can not be public."))

    class Meta:
        verbose_name = _("Discount")
        verbose_name_plural = _("Discounts")
        ordering = ("position",)
        db_table = "discount"


class Cart(TimeStampedBaseModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    is_alive = models.BooleanField(default=True)
    user = models.ForeignKey(Profile, on_delete=models.RESTRICT, related_name="carts", verbose_name=_("user"))

    main_fk_field = "user"

    def __str__(self):
        return f"{self.user.public_name} - {self.created_at}"

    def save(self, *args, **kwargs):
        if self.is_alive:
            Cart.objects.filter(is_alive=True, user=self.user).exclude(id=self.id).update(is_alive=False)
        super().save(*args, **kwargs)

    def total_value(self):
        total_value = self.items.aggregate(total_value=Sum(F("food__price") * F("count")))["total_value"]
        return total_value

    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")
        ordering = ("position",)
        db_table = "cart"


class CartItem(TimeStampedBaseModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    food = models.ForeignKey(Food, on_delete=models.RESTRICT, related_name="cart_items", verbose_name=_("food"))
    count = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name=_("count"))
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items", verbose_name=_("cart"))

    main_fk_field = "cart"

    def __str__(self):
        return f"{self.cart.__str__()} - {self.food.name}"

    class Meta:
        verbose_name = _("Cart Item")
        verbose_name_plural = _("Cart Items")
        ordering = ("position",)
        db_table = "cart item"


class Order(TimeStampedBaseModel):
    STATUS_CREATED = "CRT"
    STATUS_READY_TO_PAY = "RTP"
    STATUS_PAID = "PD"
    STATUS_REJECTED = "RJC"
    STATUS_IN_PROGRESS = "IPR"
    STATUS_DELIVERED = "DLV"

    STATUS_CHOICES = (
        (STATUS_CREATED, "created"),
        (STATUS_READY_TO_PAY, "ready to pay"),
        (STATUS_PAID, "paid"),
        (STATUS_REJECTED, "rejected"),
        (STATUS_IN_PROGRESS, "in progress"),
        (STATUS_DELIVERED, "delivered"),
    )

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    cart = models.OneToOneField(Cart, editable=False, on_delete=models.RESTRICT, related_name="order",
                                verbose_name=_("cart"))
    discount = models.ForeignKey(Discount, on_delete=models.RESTRICT, related_name="orders", blank=True, null=True,
                                 verbose_name=_("discount"))
    has_delivery = models.BooleanField(blank=True, null=True, default=None, verbose_name=_("has_delivery"))
    address = models.CharField(max_length=256, blank=True, null=True, verbose_name=_("address"))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CREATED,
                              verbose_name=_("status"))
    final_value = models.FloatField(verbose_name=_("total value"))

    def __str__(self):
        return f"{self.cart.__str__()} order"

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        ordering = ("position",)
        db_table = "order"
        indexes = [
            models.Index(fields=["position"]),
            models.Index(fields=["created_at"])
        ]


class Payment(TimeStampedBaseModel):
    order = models.ForeignKey(Order, on_delete=models.RESTRICT, related_name="payments", verbose_name=_("order"))
    is_income = models.BooleanField(default=True, verbose_name=_("is income"))
    tracking_code = models.CharField(max_length=256, verbose_name=_("tracking code"))
    payment_data = models.TextField(blank=True, null=True, verbose_name=_("payment data"))

    main_fk_field = "order"

    def __str__(self):
        if self.is_income:
            type_str = "income"
        else:
            type_str = "withdrawal"
        return f"{self.order.cart.__str__()} {type_str} payment"

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")
        ordering = ("position",)
        db_table = "payment"
