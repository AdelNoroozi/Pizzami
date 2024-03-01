from django.contrib import admin

from pizzami.common.admin import BaseModelAdmin
from pizzami.feedback.models import Comment


@admin.register(Comment)
class CommentModelAdmin(BaseModelAdmin):
    list_display = ["__str__", "is_confirmed", "parent"] + BaseModelAdmin.list_display
    list_editable = ["is_confirmed"] + BaseModelAdmin.list_editable
    list_filter = BaseModelAdmin.list_filter + ["food", "user", "parent", "is_confirmed", "by_staff"]
    search_fields = ["text"]
