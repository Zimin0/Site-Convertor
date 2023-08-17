from django.urls import path
from users.views import code, register, good_code, need_to_pay, clear, login
from django.conf.urls.i18n import i18n_patterns

app_name = 'users'

urlpatterns = [
    path('register/', register, name='register'), # форма регистрации
    path('register/<str:phone>', register, name='register'), # форма регистрации, на которую перешли после ввода телефона в форме входа
    path('login/', login, name='login'), # форма входа
    path('code/', code, name='code'), # поле ввода смс кода
    path('good_code/', good_code, name='good_code'), # код введен правильно 
    path('need-to-pay/', need_to_pay, name='need_to_pay'), # нужно оплатить 2ю конвертацию !!! need_to_pay_back_to
    path('clear/', clear) # для дебага - удаляет данные сессии
]
