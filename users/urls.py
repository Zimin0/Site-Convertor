from django.urls import path
from users.views import phone

app_name = 'users'

urlpatterns = [
    path('phone/<str:order_id>/', phone, name='phone'),
]