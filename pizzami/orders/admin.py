from typing import Optional

from admin_numeric_filter.admin import NumericFilterModelAdmin, SliderNumericFilter
from django.contrib import admin
from django.http import HttpRequest

from pizzami.common.admin import BaseModelAdmin
from pizzami.orders.models import Discount, Order, Payment


@admin.register(Discount)
class DiscountAdmin(BaseModelAdmin, NumericFilterModelAdmin):
    list_display = ["name", "is_public", "type", "specified_to_type", "absolute_value",
                    "percentage_value"] + BaseModelAdmin.list_display
    list_editable = BaseModelAdmin.list_editable + ["is_public", "absolute_value", "percentage_value"]
    list_filter = BaseModelAdmin.list_filter + ["type", "is_public", "specified_to_type",
                                                ("absolute_value", SliderNumericFilter),
                                                ("percentage_value", SliderNumericFilter)]
    search_fields = ["name", "description"]
    ordering = BaseModelAdmin.ordering + ["absolute_value", "percentage_value"]


@admin.register(Order)
class OrderAdmin(BaseModelAdmin, NumericFilterModelAdmin):
    list_display = ["__str__", "status", "final_value"] + BaseModelAdmin.list_display
    list_editable = BaseModelAdmin.list_editable + ["status"]
    list_filter = BaseModelAdmin.list_filter + ["status", "cart__user",
                                                ("final_value", SliderNumericFilter)]
    search_fields = ["__str__"]
    ordering = BaseModelAdmin.ordering + ["final_value"]

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Optional = ...) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj: Optional = ...) -> bool:
        return False


@admin.register(Payment)
class PaymentAdmin(BaseModelAdmin, NumericFilterModelAdmin):
    list_display = ["__str__", "get_final_value"] + BaseModelAdmin.list_display
    list_editable = []
    list_filter = BaseModelAdmin.list_filter + ["is_income"]
    search_fields = ["__str__"]

    @admin.display(ordering="order__final_value")
    def get_final_value(self, obj):
        return obj.order.final_value

    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    def has_delete_permission(self, request: HttpRequest, obj: Optional = ...) -> bool:
        return False

    def has_change_permission(self, request: HttpRequest, obj: Optional = ...) -> bool:
        return False
