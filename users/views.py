from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.models import User
from users.models import Profile
from convert_order.models import ConvertOrder
from files.models import File
from django.views import View
from payment.sms_sender import send_confiramtion_code

# class PhoneView(View):
#     """ Отображение страницы ввода номера телефона. """

#     def get(self, request, order_id):
#         return render(request, 'users/phone.html')

#     def post(self, request, order_id):
#         decrypted_id = ConvertOrder.decrypt_id(order_id) # расшифровываем order_id в int
#         order = get_object_or_404(ConvertOrder, id=decrypted_id)

#         cur_user_profile = Profile.objects.filter(phone=request.POST['phone']) 

#         ### Такой юзер уже существует ###
#         if cur_user_profile.exists(): 
#             cur_user = cur_user_profile.first().user # Подтягиваем модель юзера

#             ### Если уже делал конвертацию ###
#             if cur_user.profile.convert_already: 
#                 return redirect('payment:payment_form')

#         ### Искомого юзера не существует ###
#         else: 
#             new_user = User.objects.create(username=f'user{order.id}')
#             new_user.save(update_fields=['username'])

#         new_user.profile.phone = request.POST['phone']
#         new_user.profile.convert_already = True
#         new_user.profile.amount_of_converts += 1
#         new_user.profile.phone_is_confirmed = True
#         new_user.profile.save(update_fields=['phone', 'convert_already', 'amount_of_converts', 'phone_is_confirmed'])
        
#         request.session['phone_confirmed'] = True
#         request.session['phone'] = request.POST['phone']
        
#         ### Тесты, удалить на продакшене!!! ###
#         source_file = File.objects.get(id=10)
#         new_file = File.objects.create(order=order, file=source_file.file, file_type='3')
#         new_file.save()
#         #######################################
#         return redirect('convert_order:phone_main', order_id=order_id)

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
    """ Страница с полем смс кода. """
    if request.session.get('phone_is_confirmed', None):
        return redirect('users:good_code')
    if not request.session.get('phone', None): # если в сессии нет номера телефона
        return redirect('users:register')
    print(request.session.items())
    print(request.session.get('confirmation_code', None))
    context = {}
    if request.method == 'POST':
        code_is_sended = request.session.get('code_is_sended', None)
        if code_is_sended is None:
            return redirect('users:register')
        code = request.POST['sms_code']
        if str(code) == str(request.session['confirmation_code']): # если введен правильный смс код
            cur_user_profile = Profile.objects.filter(phone=request.session['phone']) 
            if cur_user_profile.exists():  # Если такой юзер уже существует 
                cur_user = cur_user_profile.first().user # Подтягиваем модель юзера
                cur_user.profile.convert_already = True
            else: 
                last_user_pk = User.objects.order_by('pk').last().pk # нужен для пронумеровки следующего юзера
                cur_user = User.objects.create(username=f'user{last_user_pk+1}')
                cur_user.save(update_fields=['username'])
            cur_user.profile.phone_is_confirmed = True
            cur_user.profile.save()
            request.session['convert_already'] = cur_user.profile.convert_already # конвертировал ли раннее данный пользователь и нужна ли оплата
            request.session['phone_is_confirmed'] = True
            request.session.pop('confirmation_code')
            request.session.pop('code_is_sended')
            return redirect('users:good_code')
        else:
            context['message'] = 'Код не совпадает! Попробуйте еще раз!'
            return render(request, 'users/code.html', context)
    elif request.method == 'GET':
        if not request.session['code_is_sended']: # если код еще не отправлялся
            request.session['code_is_sended'] = True
            request.session['confirmation_code'] = send_confiramtion_code(request.session['phone'] ) # оправляет код смс на телефон
            print(f'Код подтверждения: {request.session["confirmation_code"]}')
            return render(request, 'users/code.html')
        else: # если код уже отправлялся
            context['message'] = 'Код уже отправлен!'
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
    return HttpResponse("Сессия очищена!")