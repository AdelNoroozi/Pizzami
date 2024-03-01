from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from pizzami.api.mixins import ApiAuthMixin, BasePermissionsMixin
from pizzami.authentication.permissions import IsAuthenticatedAndNotAdmin
from pizzami.feedback.documentation import RATE_FOOD_DESCRIPTION, RATE_FOOD_RESPONSES, CREATE_COMMENT_RESPONSES, \
    GET_COMMENTS_DESCRIPTION, GET_COMMENTS_PARAMETERS, GET_COMMENTS_RESPONSES
from pizzami.feedback.serializers import RatingInputSerializer, CommentInputSerializer
from pizzami.feedback.services import create_or_update_rating, create_comment, get_comments, confirm_comment


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
        description=GET_COMMENTS_DESCRIPTION,
        parameters=GET_COMMENTS_PARAMETERS,
        responses=GET_COMMENTS_RESPONSES
    )
    def get(self, request):
        query_dict = request.GET
        user = request.user
        if not query_dict.get("set") == "mine":
            if not user.is_staff:
                return Response(data={"error": "non staff users can only access their own comments"},
                                status=status.HTTP_403_FORBIDDEN)
            data = get_comments(query_dict=query_dict, is_user_staff=True)
        else:
            if user.is_staff:
                return Response(data={"error": "only authenticated normal users can access their own comments"},
                                status=status.HTTP_403_FORBIDDEN)
            data = get_comments(query_dict=query_dict, is_user_staff=False, user=user)
        return Response(data=data, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["Feedback"],
        request=CommentInputSerializer,
        responses=CREATE_COMMENT_RESPONSES
    )
    def post(self, request):
        comment_data = create_comment(data=request.data, user=request.user)
        return Response(data=comment_data, status=status.HTTP_201_CREATED)


class CommentConfirmAPI(ApiAuthMixin, BasePermissionsMixin, APIView):
    permissions = {
        "PATCH": [IsAdminUser]
    }

    @extend_schema(
        tags=["Feedback"]
    )
    def patch(self, request, **kwargs):
        comment_id = kwargs.get("id")
        action = kwargs.get("action")
        comment_confirmation = confirm_comment(comment_id=comment_id, action=action)
        if comment_confirmation:
            return Response(data={"message": f"Comment {action}ed successfully"}, status=status.HTTP_200_OK)
        if comment_confirmation is None:
            return Response(data={"message": f"Comment is already {action}ed"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={"message": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)
