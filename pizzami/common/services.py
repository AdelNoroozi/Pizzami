import uuid

from django.db.models.base import ModelBase
from rest_framework.generics import get_object_or_404


def change_activation_status(obj_id: uuid, obj_cls: ModelBase) -> bool:
    obj = get_object_or_404(obj_cls, id=obj_id)
    is_active = obj.is_active
    obj.is_active = not is_active
    obj.save()
    return not is_active
