from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

admin.autodiscover()

i18n_urls  = (
    path('', include('convert_order.urls')),
    path('admin/', admin.site.urls),
    path('payment/', include('payment.urls')),
    path('file/', include('files.urls')),
    path('users/', include('users.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
)

urlpatterns = [
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns.extend(i18n_patterns(*i18n_urls, prefix_default_language=False))