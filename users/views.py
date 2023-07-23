from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.models import User
from users.models import Profile
from convert_order.models import ConvertOrder
from files.models import File
from django.views import View

class PhoneView(View):
    """ Отображение страницы ввода номера телефона. """

    def get(self, request, order_id):
        return render(request, 'users/phone.html')

    def post(self, request, order_id):
        decrypted_id = ConvertOrder.decrypt_id(order_id) # расшифровываем order_id в int
        order = get_object_or_404(ConvertOrder, id=decrypted_id)

        cur_user_profile = Profile.objects.filter(phone=request.POST['phone']) 

        ### Такой юзер уже существует ###
        if cur_user_profile.exists(): 
            cur_user = cur_user_profile.first().user # Подтягиваем модель юзера

            ### Если уже делал конвертацию ###
            if cur_user.profile.convert_already: 
                return redirect('payment:payment_form')

        ### Искомого юзера не существует ###
        else: 
            new_user = User.objects.create(username=f'user{order.id}')
            new_user.save(update_fields=['username'])

        new_user.profile.phone = request.POST['phone']
        new_user.profile.convert_already = True
        new_user.profile.amount_of_converts += 1
        new_user.profile.phone_is_confirmed = True
        new_user.profile.save(update_fields=['phone', 'convert_already', 'amount_of_converts', 'phone_is_confirmed'])
        
        request.session['phone_confirmed'] = True
        request.session['phone'] = request.POST['phone']
        
        ### Тесты, удалить на продакшене!!! ###
        source_file = File.objects.get(id=10)
        new_file = File.objects.create(order=order, file=source_file.file, file_type='3')
        new_file.save()
        #######################################

        return redirect('convert_order:phone_main', order_id=order_id)

