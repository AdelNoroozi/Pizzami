from django.urls import path

from pizzami.feedback.apis import RateFoodAPI, CommentsAPI, CommentConfirmAPI, CommentAPI

urlpatterns = [
    path('rate-food/', RateFoodAPI.as_view(), name="rate_food"),
    path('comments/', CommentsAPI.as_view(), name="comments"),
    path('comments/<str:id>/', CommentAPI.as_view(), name="comment"),
    path('comments/<str:id>/<str:action>/', CommentConfirmAPI.as_view(), name="confirm_comment"),
]
