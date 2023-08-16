from django.urls import path
from payment.views import payment_form, catch_payment, load
from django.conf.urls.i18n import i18n_patterns

app_name = 'payment'

urlpatterns = [
    path('', payment_form, name='payment_form'),
    path('catch-payment/', catch_payment, name='catch_payment'),
    path('load/', load, name='load')
]
