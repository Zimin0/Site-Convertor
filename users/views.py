from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.models import User
from users.models import Profile
from convert_order.models import ConvertOrder

from convert_order.models import ConvertOrder
def phone(request, order_id):
    """ Страница с формой ввода номера телефона. """

    context = {}

    decrypted_id = ConvertOrder.decrypt_id(order_id)
    order = get_object_or_404(ConvertOrder, id=decrypted_id) # Оптимизировать запрос
    
    if request.method == 'POST':
        ## Если юзер уже существует ##
        cur_user_profile = Profile.objects.filter(phone=request.POST['phone']) # (<Chapter: Telemachus>, False)
        if cur_user_profile.count() > 0:
            print("Такой юзер уже существует!")
            if cur_user_profile.convert_already: # если уже делал конвертацию 
                return HttpResponse("Плоти, сука!")
            else: # если еще не делал конвертацию
                print('еще не делал конвертацию ')
                cur_user = cur_user_profile.user 
                cur_user_profile.phone = request.POST['phone']
                cur_user_profile.convert_already = True
                cur_user_profile.amount_of_converts += 1
                cur_user.save()
                return redirect('convert_order:phone_main', order_id=order.id, phone_confirmed=1) 
        else: # !!!! правильно создать юзера !!!!
            print("такого юзера не существует")
            new_user = User.objects.create(username=f'user{order.id}')
            new_user.save()
            new_user.profile.phone = request.POST['phone']

        return redirect('convert_order:phone_main', order_id=order_id, phone_confirmed=1) 
    return render(request, 'users/phone.html', context)
