from pizzami.users.models import BaseUser, Profile


def create_profile(user: BaseUser, bio: str | None, public_name: str) -> Profile:
    return Profile.objects.create(user=user, bio=bio, public_name=public_name)


def get_profile(user: BaseUser) -> Profile:
    return Profile.objects.get(user=user)
