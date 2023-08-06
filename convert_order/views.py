from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext as _
from django.utils.translation import activate # activate('en')

from convert_order.models import ConvertOrder
from files.models import File
from users.models import Profile

def clear_main(request):
    """ Отображает страницу для загрузки файлов. """
    context = {}
    context['files_uploaded'] = False
    if not request.session.get('phone_is_confirmed', None): # если None или False
        print("Подтягиваю данные из сессии!")
        request.session['phone_is_confirmed'] = False 
        request.session['convert_already'] = False
        request.session['amount_of_convertations'] = 0

    print('Все кукисы =',request.COOKIES.keys())
    if 'phone' in request.COOKIES:
        print("Подтягиваю телефон из кукисов!")
        request.session['phone'] = request.COOKIES['phone']
        request.session['phone_is_confirmed'] = True
        request.session['amount_of_convertations'] = request.COOKIES['amount_of_convertations'] 
        request.session['convert_already'] = request.COOKIES['convert_already']
    else:
        print("Телефона в кукисах нет!")
    print("Сессия:",request.session.items())
    if request.method == 'POST':
        if len(request.FILES) < 2: # если загружено меньше, чем 2 файла
            context['message'] = _('Upload 2 files!') 
            return render(request, 'convert_order/index.html', context)
        file1 = request.FILES['file1']
        file2 = request.FILES['file2']
        print(f'Загружены файлы {file1} и {file2}.')
        context['message'] = _('Files {} and {} were uploaded!').format(file1.name, file2.name) # можно удалить, т к не отображается на странице

        #### Создаем новый заказ на конвертацию и добавляем файлы ####
        order = ConvertOrder() 
        order.save() 
        File.objects.create(order=order , file=file1, file_type='1').save()
        File.objects.create(order=order, file=file2, file_type='2').save()
        #### Только для тестирования ####
        File.objects.create(order=order, file=file2, file_type='3').save()
        ##############################################################
        encrypted_id = ConvertOrder.crypt_id(order.id)
        return redirect('convert_order:files_main', order_id=encrypted_id)
    
    return render(request, 'convert_order/index.html', context)

def files_main(request, order_id):
    """ Главная страница с загруженныии файлыми."""
    print(request.POST)
    print(request.session.items())
    print(f'order_id = {order_id}')

    context = {}
    phone_is_confirmed = request.session.get('phone_is_confirmed', False)
    context['phone_is_confirmed'] = phone_is_confirmed
    context['files_uploaded'] = True
    context['order_id'] = order_id 
    if phone_is_confirmed:
        decrypted_id = ConvertOrder.decrypt_id(order_id)
        order = get_object_or_404(ConvertOrder, id=decrypted_id)
        user_profile = get_object_or_404(Profile, phone=order.phone)
        order.phone = request.session['phone']
        order.save()
        # достаем кол-во оставшихся бесплатных скачиваний
        context['amount_of_convertations'] = user_profile.amount_of_converts 
        context['convert_already'] = request.session['convert_already']
    else:
        context['amount_of_convertations'] = 0
        context['convert_already'] = False
    print(f'context={context}')
    return render(request, 'convert_order/index.html', context) 



