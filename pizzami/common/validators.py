from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def string_ending_validator(field_name: str, str_value: str, ending_str: str):
    if not str_value.endswith(ending_str):
        raise ValidationError(
            _(f"{field_name}s must end with '{ending_str}'"),
            code="invalid_string_ending"
        )


def string_included_validator(field_name: str, str_value: str, including_str: str, included_helper: str):
    if including_str not in str_value:
        raise ValidationError(
            _(f"{field_name}s must include {included_helper}"),
            code="invalid_string_format"
        )
