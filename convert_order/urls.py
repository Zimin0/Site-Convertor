from django.urls import path, include
from convert_order.views import clear_main, phone_main, load_file

app_name = 'convert_order'

urlpatterns = [
    
    path('', clear_main, name='clear_main'),
    path('<str:order_id>/', phone_main, name='phone_main'),  
    path('file/<str:order_id>/', load_file, name='file'),  
]
