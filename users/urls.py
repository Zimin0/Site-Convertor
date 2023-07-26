from django.urls import path
from users.views import code, register, good_code, need_to_pay

app_name = 'users'

urlpatterns = [
    path('register/', register, name='register'), # поле ввода номера телефона
    path('code/', code, name='code'), # поле ввода смс кода
    path('good_code/', good_code, name='good_code'), # код введен правильно 
    path('need_to_pay/', need_to_pay, name='need_to_pay'), # нужно оплатить 2ю конвертацию
]
