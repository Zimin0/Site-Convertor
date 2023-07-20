from django.contrib import admin
from django.urls import path, include
from convert_order.views import show_order, converter

urlpatterns = [
    path('', converter, ),
    path('orders/', show_order, ),
]
