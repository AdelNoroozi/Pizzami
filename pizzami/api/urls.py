from django.urls import path, include

urlpatterns = [
    path('users/', include('pizzami.users.urls')),
    path('auth/', include('pizzami.authentication.urls')),
    path('ingredients/', include('pizzami.ingredients.urls')),
    path('foods/', include('pizzami.foods.urls')),
]
