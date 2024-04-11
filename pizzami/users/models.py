import uuid

from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from pizzami.common.models import TimeStampedBaseModel
from pizzami.core.cache import invalidate_cache
from pizzami.users.managers import BaseUserManager


class BaseUser(TimeStampedBaseModel, AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(verbose_name = "email address",
                              unique=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = BaseUserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        indexes = [
            models.Index(fields=["email"])
        ]


class Profile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name="profile", verbose_name=_("user"))
    bio = models.CharField(max_length=1000, null=True, blank=True, verbose_name=_("bio"))
    public_name = models.CharField(max_length=50, unique=True, verbose_name=_("public name"))

    def save(self, *args, **kwargs):
        profile_cache_key = f"get_profile:():{{'user': <BaseUser: {self.user.email}>}}"
        invalidate_cache(profile_cache_key)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} profile"


class Address(TimeStampedBaseModel):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="addresses", verbose_name=_("user"))
    title = models.CharField(max_length=32, verbose_name=_("title"))
    address_str = models.TextField(verbose_name=_("address str"))
    phone_number = PhoneNumberField(verbose_name=_("phone number"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")
        ordering = ("position",)
        db_table = "address"
