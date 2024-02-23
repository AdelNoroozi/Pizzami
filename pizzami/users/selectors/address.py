from pizzami.users.models import Profile, Address


def get_addresses_by_user(user: Profile):
    return Address.objects.active().filter(user=user)
