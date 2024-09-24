from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('apps.authentication.api.urls')),
    # path('api/v1/orders/', include('apps.orders.api.urls')),
    path('api/v1/products/', include('apps.catalog.api.urls')),
    path('api/v1/pages/', include('apps.pages.api.urls')),
    path('api/v1/chat/', include('apps.support_admin_chat.api.urls')),
    path('support/', include('apps.support_admin_chat.urls')),
]

urlpatterns += [
    path("", include("apps.openapi.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
