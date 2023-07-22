from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('convert_order.urls')),
    path('payment/', include('payment.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
]

""" 
URL MAP
"""
