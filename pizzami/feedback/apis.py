from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from pizzami.api.mixins import ApiAuthMixin, BasePermissionsMixin
from pizzami.authentication.permissions import IsAuthenticatedAndNotAdmin
from pizzami.feedback.documentation import RATE_FOOD_DESCRIPTION, RATE_FOOD_RESPONSES
from pizzami.feedback.serializers import RatingInputSerializer, CommentInputSerializer
from pizzami.feedback.services import create_or_update_rating, create_comment


class RateFoodAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "PUT": [IsAuthenticatedAndNotAdmin]
    }

    @extend_schema(
        tags=['Feedback'],
        request=RatingInputSerializer,
        description=RATE_FOOD_DESCRIPTION,
        responses=RATE_FOOD_RESPONSES
    )
    def put(self, request):
        serializer = RatingInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_or_update_rating(food_id=serializer.data["food"], user=request.user, rate=serializer.data["rate"])
        return Response(data={"message": "done"}, status=status.HTTP_200_OK)


class CommentsAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "GET": [IsAuthenticated],
        "POST": [IsAuthenticatedAndNotAdmin]
    }

    @extend_schema(
        tags=["Feedback"],
        request=CommentInputSerializer
    )
    def post(self, request):
        comment_data = create_comment(data=request.data, user=request.user)
        return Response(data=comment_data, status=status.HTTP_201_CREATED)
