from django.urls import path

from pizzami.orders.apis import DiscountsAPI

urlpatterns = [
    path('discounts/', DiscountsAPI.as_view(), name='discounts')
]
