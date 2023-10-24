from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def string_ending_validator(field_name: str, str_value: str, ending_str: str):
    if not str_value.endswith(ending_str):
        raise ValidationError(
            _(f"{field_name}s must end with {ending_str}"),
            code="invalid_string_ending"
        )
