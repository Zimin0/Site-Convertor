from django.urls import path
from users.views import bad_code, code, register, good_code

app_name = 'users'

urlpatterns = [
    path('register', register, name='register'), # поле ввода номера телефона
    path('code/', code, name='code'), # поле ввода смс кода
    path('bad_code/', bad_code, name='bad_code'), # код введен неправильно 
    path('good_code/', good_code, name='good_code'), # код введен правильно
]
