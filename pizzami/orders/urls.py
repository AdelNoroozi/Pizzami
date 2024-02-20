from django.urls import path

from pizzami.orders.apis import DiscountsAPI, DiscountAPI, AddToCartAPI, MyCartAPI

urlpatterns = [
    path('discounts/', DiscountsAPI.as_view(), name='discounts'),
    path('discounts/<str:id>/', DiscountAPI.as_view(), name='discount'),
    path('add-to-cart/', AddToCartAPI.as_view(), name='add_to_cart'),
    path('my-cart/', MyCartAPI.as_view(), name='my_cart')
]
