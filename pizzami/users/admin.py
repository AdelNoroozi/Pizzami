from django.contrib import admin

from pizzami.users.models import BaseUser, Profile

admin.site.register(BaseUser)
admin.site.register(Profile)
