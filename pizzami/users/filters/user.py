from django_filters import FilterSet

from pizzami.users.models import BaseUser


class UserFilter(FilterSet):
    class Meta:
        model = BaseUser
        fields = {
            "is_active": ["exact"],
            "is_admin": ["exact"],
            "is_superuser": ["exact"]
        }
