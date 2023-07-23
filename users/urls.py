from django.urls import path
from users.views import PhoneView

app_name = 'users'

urlpatterns = [
    path('phone/<str:order_id>/', PhoneView.as_view(), name='phone'),
]
