from django.urls import path
from support.views import support

app_name = 'support'

urlpatterns = [
    path('', support, name='support'),
]
