"""final URL Configuration"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from analyse import views as analyse_views, api_views

router = DefaultRouter()
router.register('analyse/organization', api_views.OrganizationViewSet, basename='organization')
router.register('analyse/product', api_views.ProductViewSet, basename='product')


urlpatterns = [
                  path('', analyse_views.Home.as_view(), name='home'),
                  path('home/', analyse_views.Home.as_view(), name='home'),
                  path('search/', analyse_views.search, name='search'),
                  path('admin/', admin.site.urls),
                  path('analyse/', include("analyse.urls")),
                  path('followup/', include("followup.urls")),
                  path('user/', include("user.urls")),
                  path('api-auth/', include('rest_framework.urls')),
                  path('api/v1/list/', include(router.urls)),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


