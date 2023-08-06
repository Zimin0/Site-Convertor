from django.urls import path, include
from convert_order.views import clear_main, files_main
from django.conf.urls.i18n import i18n_patterns

app_name = 'convert_order'

urlpatterns = [
    path('', clear_main, name='clear_main'),

    path('<str:order_id>/', files_main, name='files_main'),  

]
