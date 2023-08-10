from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.generic import RedirectView
from django.views.i18n import JavaScriptCatalog

admin.autodiscover()

i18n_urls  = (

)

urlpatterns = [
    path('admin/', admin.site.urls), # 1
    path('favicon.ico/', RedirectView.as_view(url='/static/convert_order/img/favicon.ico')), # 2
    ]

urlpatterns += i18n_patterns(
    path('', include('convert_order.urls')), # 3
    path("i18n/", include("django.conf.urls.i18n")), # 4
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('payment/', include('payment.urls')),
    path('file/', include('files.urls')),
    path('users/', include('users.urls')), 
    path('support/', include('support.urls')), 
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#urlpatterns.extend(i18n_patterns(*i18n_urls))


# from django.contrib import admin
# from django.urls import path, include
# from django.conf import settings
# from django.conf.urls.static import static
# from django.conf.urls.i18n import i18n_patterns
# from django.views.generic import RedirectView

# admin.autodiscover()

# i18n_urls  = (
#     path("i18n/", include("django.conf.urls.i18n")), # 4
#     path('payment/', include('payment.urls')),
#     path('file/', include('files.urls')),
#     path('users/', include('users.urls')), 
# )

# urlpatterns = [
#     path('admin/', admin.site.urls), # 1
#     path('favicon.ico/', RedirectView.as_view(url='/static/convert_order/img/favicon.ico')), # 2
#     ]

# urlpatterns += i18n_patterns(
#     path('', include('convert_order.urls')), # 3
# )

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns.extend(i18n_patterns(*i18n_urls))