from django.contrib import admin

from pizzami.common.admin import BaseModelAdmin
from pizzami.users.models import BaseUser, Profile, Address

admin.site.register(Profile)


@admin.register(Address)
class AddressAdmin(BaseModelAdmin):
    list_display = ["title", "user", "phone_number"] + BaseModelAdmin.list_display
    list_filter = BaseModelAdmin.list_filter + ["user"]
    search_fields = ["title", "address_str"]


@admin.register(BaseUser)
class BaseUserAdmin(BaseModelAdmin):
    list_display = ["email", "is_admin", "is_superuser"] + BaseModelAdmin.list_display
    list_editable = BaseModelAdmin.list_editable + ["is_admin", "is_superuser"]
    list_filter = BaseModelAdmin.list_filter + ["is_admin", "is_superuser"]
    search_fields = ["email", "profile__public_name"]
