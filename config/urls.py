from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import RedirectView

admin.autodiscover()

i18n_urls  = (
    #path('favicon.ico/', ),
    path("i18n/", include("django.conf.urls.i18n")),
    path('payment/', include('payment.urls')),
    path('file/', include('files.urls')),
    path('users/', include('users.urls')), 
)

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('favicon.ico/', RedirectView.as_view(url='/static/convert_order/img/favicon.ico')),
    ] 

urlpatterns += i18n_patterns(
    path('', include('convert_order.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns.extend(i18n_patterns(*i18n_urls, prefix_default_language=False))