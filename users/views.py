from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.models import User
from users.models import Profile
from convert_order.models import ConvertOrder
from production_settings.models import ProductionSettings
from payment.sms_sender import send_confiramtion_code
from django.utils.translation import gettext as _
from django.utils.translation import activate 

def login(request):
    """ Страница с полем ввода номера телефона. """
    context = {}
    if request.session.get('phone_is_confirmed', None):
        return redirect('users:good_code')
    if request.session.get('back_to', None):
        context['need_to_back'] = True
        context['order_id'] = request.session['back_to'] # достаем order_id
    if request.method == 'POST':
        phone = request.POST['phone'] # подтягиваем введенный телефон
        request.session['phone'] = phone
        user_is_found = Profile.objects.filter(phone=phone).exists()
        if user_is_found: # если в базе данных уже есть такой телефон
            request.session['code_is_sended'] = False
            print(f"Введен телефон: {phone}")
            return redirect('users:code')
        else: # иначе перенаправляем с сохранением введенного телефона
            return redirect('users:register', phone)
    return render(request, 'users/login.html', context)

def register_back_to(request, order_id):
    print('Вижу order_id в регистре ')
    request.session['back_to'] = order_id # вернуться на страницу конвертации этого заказа
    return redirect('users:register')

def login_back_to(request, order_id):
    print('Вижу order_id в логине ')
    request.session['back_to'] = order_id # вернуться на страницу конвертации этого заказа
    return redirect('users:login')

def need_to_pay_back_to(request, order_id):
    print('Вижу order_id в регистре ')
    request.session['back_to'] = order_id # вернуться на страницу конвертации этого заказа
    return redirect('users:need_to_pay')

def register(request, phone=None, order_id=None):
    """ Страница с формой регистрации. """
    context = {}
    context['phone'] = ''
    print("На странице register получен номер телефона ", phone)
    if request.session.get('back_to', None):
        context['need_to_back'] = True
        context['order_id'] = request.session['back_to'] # достаем order_id
    if request.session.get('phone_is_confirmed', None):
        return redirect('users:good_code')
    if request.method == 'POST':
        ### Подтягиваем введенный данные ###
        request.session['name'] = request.POST['name']
        request.session['mail'] = request.POST['mail']
        request.session['phone'] = request.POST['phone']
        request.session['code_is_sended'] = False # ????????
        print(f"Введен телефон: {request.session['phone']}")
        return redirect('users:code')
    elif request.method == 'GET':
        if phone is not None: # если был переход со страницы входа и такого номера не зарегестрировано - заносим его в поле
            context['phone'] = phone
            return render(request, 'users/register.html', context)
    return render(request, 'users/register.html', context)

def code(request):
    """ Страница с полем смс кода. """
    if request.session.get('phone_is_confirmed', None):
        return redirect('users:good_code')
    if not request.session.get('phone', None): # если в сессии нет номера телефона
        return redirect('users:register')
    print("Сессия:", request.session.items())
    print(request.session.get('confirmation_code', None))
    context = {}
    if request.session.get('back_to', None):
        context['need_to_back'] = True
        context['order_id'] = request.session['back_to'] # достаем order_id
    context['message'] = _('Code has been sent!')
    if request.method == 'POST':
        code_is_sended = request.session.get('code_is_sended', None)
        if code_is_sended is None: # Если пользователь попал на данную старницу случайно 
            return redirect('users:register')
        code = request.POST['sms_code']
        if str(code) == str(request.session.get('confirmation_code', 'No code found!')): # если введен правильный смс код
            cur_user_profile = Profile.objects.filter(phone=request.session.get('phone', 'No phone found!')) 
            if cur_user_profile.exists():  # Если такой юзер уже существует 
                cur_user = cur_user_profile.first().user # Подтягиваем модель юзера
            else: # если искомого юзера не существует - создаем нового 
                last_user_pk = User.objects.order_by('pk').last().pk # нужен для пронумеровки следующего юзера
                cur_user = User.objects.create(username=f'user{last_user_pk+1}')
                cur_user.save(update_fields=['username'])
            cur_user.profile.phone_is_confirmed = True
            cur_user.profile.phone = request.session.get('phone', 'No phone found!')
            cur_user.first_name = request.session.get('name', 'No name found!')
            cur_user.email = request.session.get('mail', 'No mail found!')
            cur_user.profile.save()
            print(request.session.keys())
            order_id = request.session.get('back_to', False)
            if order_id:
                decrypted_id = ConvertOrder.decrypt_id(order_id)
                order = get_object_or_404(ConvertOrder, id=decrypted_id)
                order.phone = request.session['phone']
                order.save()
            request.session['phone_is_confirmed'] = True
            request.session.pop('confirmation_code')
            request.session.pop('code_is_sended')
            
            response = redirect('users:good_code')
            print("Заношу телефон в кукисы!") 
            response.set_cookie('phone', request.session.get('phone', 'No phone found!')) 
            return response
        else:
            context['message'] = _('The code doesn`t match.Try again.') 
            return render(request, 'users/code.html', context)
    elif request.method == 'GET':
        if not request.session['code_is_sended']: # если код еще не отправлялся
            request.session['code_is_sended'] = True
            request.session['confirmation_code'] = send_confiramtion_code(request.session.get('phone', 'No phone found!')) # оправляет код смс на телефон
            print(f'Код подтверждения: {request.session["confirmation_code"]}')
            return render(request, 'users/code.html', context)
        else: # если код уже отправлялся
            context['message'] = _('The code has already been sent!') # Код уже отправлен!
            return render(request, 'users/code.html', context)

def good_code(request):
    """ Страница с "код подтврежден" и кнопкой закрыть."""
    context = {}
    if not request.session.get('phone_is_confirmed', None):
        return redirect('users:login')
    if request.session.get('back_to', None):
        context['need_to_back'] = True
        context['order_id'] = request.session['back_to'] # достаем order_id
    print('context in good_code', context)
    return render(request, 'users/good_code.html', context)

def need_to_pay(request):
    """ Страница с "Вы уже конвертировали у нас на сайте... Нужно оплатить" """
    context = {
        "euro_price": get_object_or_404(ProductionSettings, slug='EURO_PRICE').value,
        "ruble_price": get_object_or_404(ProductionSettings, slug='RUBLE_PRICE').value,
        "dollar_price": get_object_or_404(ProductionSettings, slug='DOLLAR_PRICE').value,
    }
    if request.session.get('back_to', None): # функционал возврата на страницу загрузки
        context['need_to_back'] = True
        context['order_id'] = request.session['back_to'] # достаем order_id
    
    if not request.session.get('phone_is_confirmed', None):
        return redirect('users:login')
    return render(request, "users/need_to_pay.html", context)

def clear(request):
    request.session.clear()
    response = HttpResponse("<h1>Сессия и кукисы очищены!</h1> <script>localStorage.clear();</script>")
    response.delete_cookie('phone')
    print('Cookies = ', response.cookies)
    print('Session = ', request.session.items()) 
    return response
