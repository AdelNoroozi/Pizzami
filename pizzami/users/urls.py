from django.urls import path

from .apis import ProfileApi, RegisterApi, MyAddressesAPI, MyAddressAPI

urlpatterns = [
    path('register/', RegisterApi.as_view(), name="register"),
    path('profile/', ProfileApi.as_view(), name="profile"),
    path('my-addresses/', MyAddressesAPI.as_view(), name="my_addresses"),
    path('my-addresses/<str:id>/', MyAddressAPI.as_view(), name="my_address")
]
