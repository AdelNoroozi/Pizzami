from django.urls import path, include

urlpatterns = [
    path('users/', include('pizzami.users.urls')),
    path('auth/', include('pizzami.authentication.urls')),
]
