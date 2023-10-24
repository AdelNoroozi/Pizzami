from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class ImageIncludedBaseModel(BaseModel):
    image_url = models.CharField(max_length=512, verbose_name=_("image url"))
    image_alt_text = models.CharField(max_length=50, verbose_name=_("image alt text"))

    class Meta:
        abstract = True
