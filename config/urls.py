from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('payment/', include('payment.urls')),
    path('file/', include('files.urls')),
    path('users/', include('users.urls')),
    path('', include('convert_order.urls')),
]

