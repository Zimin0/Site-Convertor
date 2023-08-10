from django.urls import path
from users.views import code, register, good_code, need_to_pay, clear, login, register_back_to, login_back_to, need_to_pay_back_to
from django.conf.urls.i18n import i18n_patterns

app_name = 'users'

urlpatterns = [
    path('register/back-to/<str:order_id>', register_back_to, name='register_back_to'), # форма регистрации, на которую перешли после конвертации
    path('register/', register, name='register'), # форма регистрации
    path('register/<str:phone>', register, name='register'), # форма регистрации, на которую перешли после ввода телефона в форме входа
    path('login/back-to/<str:order_id>', login_back_to, name='login_back_to'), # форма входа, на которую перешли после конвертации 
    path('login/', login, name='login'), # форма входа
    path('code/', code, name='code'), # поле ввода смс кода
    path('good_code/', good_code, name='good_code'), # код введен правильно 
    path('need-to-pay/', need_to_pay, name='need_to_pay'), # нужно оплатить 2ю конвертацию !!! need_to_pay_back_to
    path('need-to-pay/back-to/<str:order_id>', need_to_pay_back_to, name='need_to_pay_back_to'), 
    path('clear/', clear) # для дебага - удаляет данные сессии
]
