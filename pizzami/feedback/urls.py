from django.urls import path

from pizzami.feedback.apis import RateFoodAPI, CommentsAPI

urlpatterns = [
    path('rate-food/', RateFoodAPI.as_view(), name="rate_food"),
    path('comments/', CommentsAPI.as_view(), name="comments"),
]
