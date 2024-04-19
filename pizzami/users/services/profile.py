from rest_framework.utils.serializer_helpers import ReturnDict

from pizzami.core.cache import redis_cache
from pizzami.users.models import BaseUser, Profile
from pizzami.users.selectors import get_profile as get_profile_selector
from pizzami.users.serializers import ProfileOutputSerializer, ProfileUpdateSerializer


@redis_cache(ttl=60 * 15)
def get_profile(user: BaseUser) -> ReturnDict:
    profile = get_profile_selector(user=user)
    return ProfileOutputSerializer(profile).data


def update_profile(user: BaseUser, data: dict) -> ReturnDict:
    serializer = ProfileUpdateSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    custom_fields = None
    if "custom_fields" in data:
        custom_fields = data.pop("custom_fields")
    profile_qs = Profile.objects.filter(user=user)
    profile_qs.update(bio=data["bio"], public_name=data["public_name"])
    profile = profile_qs.first()
    if custom_fields is not None:
        pass
    return ProfileOutputSerializer(profile).data
