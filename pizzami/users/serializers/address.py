from rest_framework import serializers

from pizzami.users.models import Address


class AddressOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ("user", )