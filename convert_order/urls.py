from django.urls import path
from convert_order.views import clear_main, files_main, info

app_name = 'convert_order'

urlpatterns = [
    path('', clear_main, name='clear_main'),
    path('info/', info, name='info'),
    path('<str:order_id>/', files_main, name='files_main'),  
]
