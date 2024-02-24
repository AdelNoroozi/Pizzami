from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from pizzami.api.mixins import ApiAuthMixin, BasePermissionsMixin
from pizzami.authentication.permissions import IsAuthenticatedAndNotAdmin
from pizzami.feedback.serializers import RatingInputSerializer
from pizzami.feedback.services import create_or_update_rating


class RateFoodAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "PUT": [IsAuthenticatedAndNotAdmin]
    }

    @extend_schema(
        tags=['Feedback'],
        request=RatingInputSerializer
    )
    def put(self, request):
        serializer = RatingInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_or_update_rating(food_id=serializer.data["food"], user=request.user, rate=serializer.data["rate"])
        return Response(data={"message": "done"}, status=status.HTTP_200_OK)
