from django.urls import path

from pizzami.feedback.apis import RateFoodAPI

urlpatterns = [
    path('rate-food/', RateFoodAPI.as_view(), name="rate_food")
]
