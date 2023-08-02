from django.urls import path, include
from files.views import load_file
from django.conf.urls.i18n import i18n_patterns

app_name = 'files'

urlpatterns = [
    path('<str:order_id>/', load_file, name='load_file'),  
]
