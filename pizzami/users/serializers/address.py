from phonenumber_field.phonenumber import PhoneNumber
from rest_framework import serializers

from pizzami.users.models import Address


class AddressOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ("user",)


class AddressInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ("title", "address_str", "phone_number")

    def create(self, validated_data):
        validated_data["user"] = self.context.get("user")
        phone_number = validated_data["phone_number"]
        validated_data["phone_number"] = PhoneNumber.from_string(phone_number=phone_number, region='IR').as_e164
        return super().create(validated_data)
