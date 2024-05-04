from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList

from config.settings.mongodb import mongodb
from pizzami.core.cache import redis_cache, invalidate_cache
from pizzami.users.models import BaseUser, Profile
from pizzami.users.selectors import get_profile as get_profile_selector, get_profile_list as get_profile_list_selector
from pizzami.users.serializers import ProfileBaseOutputSerializer, ProfileUpdateSerializer, ProfileFullOutputSerializer, \
    ProfilePageOutputSerializer, ProfileReferenceSerializer

profile_collection = mongodb["profiles"]


@redis_cache(ttl=60 * 15)
def get_profile(user: BaseUser) -> ReturnDict:
    profile = get_profile_selector(user=user)
    return ProfileBaseOutputSerializer(profile).data


def get_full_profile(profile: Profile, is_self: bool) -> ReturnDict:
    if is_self:
        serializer = ProfileFullOutputSerializer
    else:
        serializer = ProfilePageOutputSerializer
    return serializer(profile).data


def update_profile_custom_fields(profile_id: int, custom_fields: dict):
    custom_fields.pop("_id", None)
    custom_fields.pop("core_profile_id", None)
    custom_fields.pop("public_name", None)
    custom_fields.pop("bio", None)
    profile_document = profile_collection.find_one({"core_profile_id": profile_id})
    if profile_document:
        old_fields = profile_document.copy()
        old_fields.pop("_id")
        old_fields.pop("core_profile_id")
        profile_collection.update_one(profile_document, {"$unset": old_fields})

    profile_collection.update_one(
        {"core_profile_id": profile_id},
        {"$set": custom_fields}
    )


def update_profile(user: BaseUser, data: dict) -> ReturnDict:
    serializer = ProfileUpdateSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    custom_fields = None
    if "custom_fields" in data:
        custom_fields = data.pop("custom_fields")
    profile_qs = Profile.objects.filter(user=user)
    profile_qs.update(**data)
    profile = profile_qs.first()
    profile_cache_key = f"get_profile:():{{'user': <BaseUser: {user.email}>}}"
    invalidate_cache(profile_cache_key)
    if custom_fields is not None:
        update_profile_custom_fields(profile_id=profile.id, custom_fields=custom_fields)
    return ProfileFullOutputSerializer(profile).data


def get_profile_list() -> ReturnDict:
    profiles = get_profile_list_selector()
    serializer = ProfileReferenceSerializer(profiles, many=True)
    return serializer.data
