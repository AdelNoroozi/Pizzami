from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from pizzami.foods.sitemaps import FoodSitemap

sitemaps = {
    "foods": FoodSitemap
}

urlpatterns = [
                  path("schema/", SpectacularAPIView.as_view(api_version="v1"), name="schema"),
                  path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
                  path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
                  path('admin/', admin.site.urls),
                  path('api/', include(('pizzami.api.urls', 'api'))),
                  path('sitemap.xml', sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
