from django.urls import path

from .apis import ProfileApi, RegisterApi, MyAddressesAPI, MyAddressAPI, CreateAdmin

urlpatterns = [
    path('register/', RegisterApi.as_view(), name="register"),
    path('add-admin/', CreateAdmin.as_view(), name="add_admin"),
    path('profile/', ProfileApi.as_view(), name="profile"),
    path('my-addresses/', MyAddressesAPI.as_view(), name="my_addresses"),
    path('my-addresses/<str:id>/', MyAddressAPI.as_view(), name="my_address")
]
