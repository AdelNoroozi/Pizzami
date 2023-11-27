from rest_framework.utils.serializer_helpers import ReturnDict

from pizzami.users.models import BaseUser
from pizzami.users.selectors import get_profile as get_profile_selector
from pizzami.users.serializers import ProfileOutputSerializer


def get_profile(user: BaseUser) -> ReturnDict:
    profile = get_profile_selector(user=user)
    return ProfileOutputSerializer(profile).data
