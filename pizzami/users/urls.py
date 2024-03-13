from django.urls import path

from .apis import ProfileApi, RegisterApi, MyAddressesAPI, MyAddressAPI, CreateAdmin, UsersAPI, UserActivateAPI, \
    RequestPasswordResetAPI

urlpatterns = [
    path('', UsersAPI.as_view(), name="users"),
    path('register/', RegisterApi.as_view(), name="register"),
    path('register/', RegisterApi.as_view(), name="register"),
    path('request-password-reset/', RequestPasswordResetAPI.as_view(), name="request_password_reset"),
    path('add-admin/', CreateAdmin.as_view(), name="add_admin"),
    path('profile/', ProfileApi.as_view(), name="profile"),
    path('my-addresses/', MyAddressesAPI.as_view(), name="my_addresses"),
    path('my-addresses/<str:id>/', MyAddressAPI.as_view(), name="my_address"),
    path('<str:id>/activate', UserActivateAPI.as_view(), name="change_user_activation_status"),
]
