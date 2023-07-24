from django.urls import path
from users.views import PhoneNumberView, PhoneView, code

app_name = 'users'

urlpatterns = [
    path('phone/<str:phone_number>/', PhoneNumberView.as_view(), name='PhoneNumberView'),
    path('check/<str:code>/', code, name='code'),
    path('phone/<str:order_id>/', PhoneView.as_view(), name='phone'),
]
