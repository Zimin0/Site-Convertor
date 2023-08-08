from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.utils.translation import gettext as _
from django.utils.translation import activate # activate('en')
from django.core.files import File

from convert_order.models import ConvertOrder
from files.models import File as My_File
from users.models import Profile
from .main_convertation_script import convert_2_files_into_new_structure
from django.core.files.uploadedfile import InMemoryUploadedFile

def clear_main(request):
    """ Отображает страницу для загрузки файлов. """
    context = {}
    request.session['cookies_is_confirmed'] = True
    context['cookies_is_confirmed'] = request.session['cookies_is_confirmed'] 
    context['files_uploaded'] = False 
    context['phone_is_confirmed'] = request.session.get('phone_is_confirmed', False) 
    if not request.session.get('phone_is_confirmed', None): # если None или False
        print("Заполняю сессию пустыми данными!")
        request.session['phone_is_confirmed'] = False 

    if 'phone' in request.COOKIES:
        print("Подтягиваю телефон и данные из кукисов!")
        request.session['phone'] = request.COOKIES['phone']
        request.session['phone_is_confirmed'] = True
    else:
        print("Телефона в кукисах нет!")
    print("Сессия:",request.session.items())

    if request.session.get('phone_is_confirmed', False): # сделать красивее 
        user_profile = get_object_or_404(Profile, phone=request.session['phone'])
        context['amount_of_convertations'] = user_profile.amount_of_converts

    if request.method == 'POST':
        if len(request.FILES) < 2: # если загружено меньше, чем 2 файла
            return render(request, 'convert_order/index.html', context)
        file1 = request.FILES['file1']
        file2 = request.FILES['file2']
        print(f'file type = {type(file2)}')
        print(f'Загружены файлы {file1} и {file2}.')

        #### Создаем новый заказ на конвертацию и добавляем файлы ####
        order = ConvertOrder() 
        order.save() 
        file1_dj = My_File.objects.create(order=order , file=file1, file_type='1')
        file2_dj = My_File.objects.create(order=order, file=file2, file_type='2')
        file1_dj.save()
        file2_dj.save()
        #### Только для тестирования ####
        file3_path = convert_2_files_into_new_structure(file1_dj.file.path, file2_dj.file.path) # получаем путь нового файла
        file3_open = open(file3_path, encoding="utf-8")
        #print(file3_open.read()) # выводит текст полностью, с нормальной кодировкой 
        file4 = InMemoryUploadedFile(file=file3_open, field_name='FileField', name='resultxml.xml', content_type='application/xml', size=2625, charset=None)
        file3 = File(file3_open) # кусок говна, ломает кодировку !!!!!!
        print( 'encoding =', file3.encoding) # encoding = utf-8
        My_File.objects.create(order=order, file=file3, file_type='3').save()
        # file3_open.close()
        ##############################################################
        encrypted_id = ConvertOrder.crypt_id(order.id)
        return redirect('convert_order:files_main', order_id=encrypted_id)
    print(" request.session.get('phone_is_confirmed', False) = ",  request.session.get('phone_is_confirmed', False))
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
        try:
            int(decrypted_id) # плавающий баг
        except Exception:
            raise ValueError
        print(f"order_id={order_id}; decrypted_id={decrypted_id}") 
        order = get_object_or_404(ConvertOrder, id=decrypted_id)
        user_profile = get_object_or_404(Profile, phone=request.session['phone'])
        order.phone = request.session['phone']
        order.save()
        # достаем кол-во оставшихся бесплатных скачиваний
        context['amount_of_convertations'] = user_profile.amount_of_converts
    else:
        context['amount_of_convertations'] = None
    print(f'context={context}')
    return render(request, 'convert_order/index.html', context) 

def info(request):
    """ Страница с описанием работы конвертора. """
    return render(request, 'convert_order/info.html')

from django.utils.translation import get_language
def video(request, video_id):
    context = {}
    curr_language = get_language()
    context['curr_language'] = curr_language
    print("Текущий язык на странице с видео:", curr_language)
    template_name = f'convert_order/video{video_id}.html'
    context['video_name'] = f'button1_{curr_language}.mp4'
    if video_id in (1, 2):
        return render(request, template_name, context)
    return render('convert_order/404.html')

