from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.models import User
from users.models import Profile
from convert_order.models import ConvertOrder
from files.models import File
from django.views import View
from payment.sms_sender import send_confiramtion_code
from django.utils.translation import gettext as _
from django.utils.translation import activate 

def register(request):
    """ Страница с полем ввода номера телефона. """
    if request.session.get('phone_is_confirmed', None):
        return redirect('users:good_code')
    if request.method == 'POST':
        request.session['phone'] = request.POST['phone']
        request.session['code_is_sended'] = False
        print(f"Введен телефон: {request.session['phone']}")
        return redirect('users:code')
    return render(request, 'users/register.html')

def code(request):
    activate('en')
    """ Страница с полем смс кода. """
    if request.session.get('phone_is_confirmed', None):
        return redirect('users:good_code')
    if not request.session.get('phone', None): # если в сессии нет номера телефона
        return redirect('users:register')
    print(request.session.items())
    print(request.session.get('confirmation_code', None))
    context = {}
    context['message'] = _('Code has been sent!')
    if request.method == 'POST':
        code_is_sended = request.session.get('code_is_sended', None)
        if code_is_sended is None: # Если пользователь попал на данную старницу случайно 
            return redirect('users:register')
        code = request.POST['sms_code']
        if str(code) == str(request.session['confirmation_code']): # если введен правильный смс код
            cur_user_profile = Profile.objects.filter(phone=request.session['phone']) 
            if cur_user_profile.exists():  # Если такой юзер уже существует 
                cur_user = cur_user_profile.first().user # Подтягиваем модель юзера
            else: # если искомого юзера не существует - создаем нового 
                last_user_pk = User.objects.order_by('pk').last().pk # нужен для пронумеровки следующего юзера
                cur_user = User.objects.create(username=f'user{last_user_pk+1}')
                cur_user.save(update_fields=['username'])
            cur_user.profile.phone_is_confirmed = True
            cur_user.profile.phone = request.session['phone']
            cur_user.profile.save()
            request.session['phone_is_confirmed'] = True
            request.session.pop('confirmation_code')
            request.session.pop('code_is_sended')
            
            print("Заношу данные в кукисы!")
            response = redirect('users:good_code') 
            response.set_cookie('amount_of_convertations', request.session['amount_of_convertations'])
            response.set_cookie('phone', request.session['phone']) 
            response.set_cookie('convert_already', request.session['convert_already']) 
            print('Cookies = ', response.cookies)
            print('Все кукисы =',request.COOKIES.keys())
            return response
        else:
            context['message'] = _('The code doesn`t match.Try again.') 
            return render(request, 'users/code.html', context)
    elif request.method == 'GET':
        if not request.session['code_is_sended']: # если код еще не отправлялся
            request.session['code_is_sended'] = True
            request.session['confirmation_code'] = send_confiramtion_code(request.session['phone'] ) # оправляет код смс на телефон
            print(f'Код подтверждения: {request.session["confirmation_code"]}')
            return render(request, 'users/code.html')
        else: # если код уже отправлялся
            context['message'] = _('Code already have sent!') # Код уже отправлен!
            return render(request, 'users/code.html', context)

def good_code(request):
    """ Страница с "код подтврежден" и кнопкой закрыть."""
    if not request.session.get('phone_is_confirmed', None):
        return redirect('users:register')
    return render(request, 'users/good_code.html')

def need_to_pay(request):
    """ Страница с "Вы уже конвертировали у нас на сайте... Нужно оплатить" """
    if not request.session.get('phone_is_confirmed', None):
        return redirect('users:register')
    return render(request, "users/need_to_pay.html")

def clear(request):
    request.session.clear()
    response = HttpResponse("<h1>Сессия и кукисы очищены!</h1>")
    response.delete_cookie('phone')
    response.delete_cookie('convert_already')
    response.delete_cookie('amount_of_converts')
    return response