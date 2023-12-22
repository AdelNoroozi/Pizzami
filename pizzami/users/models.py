from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from pizzami.common.models import TimeStampedBaseModel
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

    def __str__(self):
        return f"{self.user} profile"
