from django.core.validators import MinValueValidator, MaxValueValidator

from rest_framework import serializers


class RatingInputSerializer(serializers.Serializer):
    food = serializers.UUIDField(required=True)
    rate = serializers.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], required=True,
                                    help_text="must be between 0 & 5. 0 means delete.")
