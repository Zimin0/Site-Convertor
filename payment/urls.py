from django.urls import path, include
from payment.views import payment

app_name = 'payment'

urlpatterns = [
    path('', payment, name='payment'),
]
