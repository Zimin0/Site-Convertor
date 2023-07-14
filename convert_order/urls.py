from django.contrib import admin
from django.urls import path, include
from convert_order.views import show_order

urlpatterns = [
    path('', show_order),
]
