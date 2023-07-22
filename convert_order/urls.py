from django.urls import path, include
from convert_order.views import orders, converter, download_file_page, download_file

app_name = 'convert_order'

urlpatterns = [
    
    path('', converter, name='converter'),
    path('download/<order_id>/', download_file_page, name='download_file_page'),  
    path('file/<order_id>/', download_file, name='download_file'),  
    path('orders/', orders, name='orders'),
]
