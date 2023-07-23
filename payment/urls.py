from django.urls import path
from payment.views import payment_form

app_name = 'payment'

urlpatterns = [
    path('', payment_form, name='payment_form'),
]
