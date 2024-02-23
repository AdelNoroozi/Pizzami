from django.contrib import admin

from pizzami.common.admin import BaseModelAdmin
from pizzami.users.models import BaseUser, Profile, Address

admin.site.register(BaseUser)
admin.site.register(Profile)


@admin.register(Address)
class AddressAdmin(BaseModelAdmin):
    list_display = ["title", "user", "phone_number"] + BaseModelAdmin.list_display
    list_filter = BaseModelAdmin.list_filter + ["user"]
    search_fields = ["title", "address_str"]
