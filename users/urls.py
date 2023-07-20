from django.urls import path, include
from users.views import phone

app_name = 'users'

urlpatterns = [
    path('phone/<int:order_id>/', phone, name='phone'),
]