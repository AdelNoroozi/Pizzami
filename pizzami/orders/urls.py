from django.urls import path

from pizzami.orders.apis import DiscountsAPI, DiscountAPI

urlpatterns = [
    path('discounts/', DiscountsAPI.as_view(), name='discounts'),
    path('discounts/<str:id>/', DiscountAPI.as_view(), name='discount')
]
