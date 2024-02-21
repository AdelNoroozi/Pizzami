from django.urls import path

from pizzami.orders.apis import DiscountsAPI, DiscountAPI, InquiryDiscountAPI, AddToCartAPI, MyCartAPI, OrdersAPI

urlpatterns = [
    path('discounts/', DiscountsAPI.as_view(), name='discounts'),
    path('discounts/inquiry/', InquiryDiscountAPI.as_view(), name='inquiry_discount'),
    path('discounts/<str:id>/', DiscountAPI.as_view(), name='discount'),
    path('add-to-cart/', AddToCartAPI.as_view(), name='add_to_cart'),
    path('my-cart/', MyCartAPI.as_view(), name='my_cart'),
    path('', OrdersAPI.as_view(), name='orders')

]
