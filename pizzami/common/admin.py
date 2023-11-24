from django.contrib.admin import ModelAdmin


class BaseModelAdmin(ModelAdmin):
    list_display = ["name", "is_active", "position", "created_at", "updated_at"]
    list_editable = ["is_active"]
    list_filter = ["is_active", "created_at", "updated_at"]
    date_hierarchy = "created_at"
    ordering = ["created_at", "updated_at", "position"]

    class Meta:
        abstract = True
