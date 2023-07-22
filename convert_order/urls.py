from django.urls import path, include
from convert_order.views import orders, clear_main, phone_main, download_file

app_name = 'convert_order'

urlpatterns = [
    
    path('', clear_main, name='clear_main'),
    path('<str:order_id>/<int:phone_confirmed>', phone_main, name='phone_main'),  
    path('file/<str:order_id>/', download_file, name='download_file'),  
    path('orders/', orders, name='orders'),
]
