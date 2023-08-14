from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import activate, gettext as _
from django.utils.translation import get_language
from django.core.files import File
from django.http import HttpResponseNotFound

import os
import logging
from convert_order.models import ConvertOrder
from files.models import File as My_File
from users.models import Profile
from django.core.files.uploadedfile import InMemoryUploadedFile
from .main_convertation_script import convert_2_files_into_new_structure


logger = logging.getLogger(__name__)

# request.COOKIES['dataflair']
# request.COOKIES.get('visits')
          
def clear_main(request):
    """ Отображает страницу для загрузки файлов. """
    logger.info('------clear_main------')
    context = {}
    context['files_uploaded'] = False 
    context['phone_is_confirmed'] = request.session.get('phone_is_confirmed', False) 
    if not request.session.get('phone_is_confirmed', False): 
        logger.info("В сессии телефона нет! phone_is_confirmed = False")
        request.session['phone_is_confirmed'] = False 
    if 'phone' in request.COOKIES:
        logger.info(f"Подтягиваю телефон - {request.session['phone']} - и данные из cookies!")
        request.session['phone'] = request.COOKIES['phone']
        request.session['phone_is_confirmed'] = True
    else:
        logger.info("Телефона в cookies нет!")
    logger.info(f"Сессия: {request.session.items()}")

    if request.session.get('phone_is_confirmed', False): 
        user_profile = Profile.objects.get(phone=request.session['phone'])
        context['amount_of_convertations'] = user_profile.amount_of_converts

    if request.method == 'POST':
        file1 = request.FILES['file1']
        file2 = request.FILES['file2']
        logger.info(f'Загружены файлы {file1} и {file2}.')
        #### Создаем новый заказ на конвертацию и добавляем В него файлы ####
        order = ConvertOrder() 
        order.save() 
        file1_dj = My_File.objects.create(order=order , file=file1, file_type='1')
        file2_dj = My_File.objects.create(order=order, file=file2, file_type='2')
        file1_dj.save()
        file2_dj.save()
        #### Только для тестирования ####
        file3_path = convert_2_files_into_new_structure(file1_dj.file.path, file2_dj.file.path) # получаем путь нового файла
        filename = os.path.basename(file3_path)
        logger.info(f'Имя нового сконвертированного файла = {filename}')
        file3_open = open(file3_path, encoding="utf-8")
        file3 = File(file3_open) # кусок говна, ломает кодировку !!!!!!
        My_File.objects.create(order=order, file=file3, file_type='3').save()
        # file4 = InMemoryUploadedFile(file=file3_open, field_name='FileField', name=filename, content_type='application/xml', size=2625, charset=None)
        #print(file3_open.read()) # выводит текст полностью, с нормальной кодировкой 
        # file3_open.close()
        ##############################################################
        encrypted_id = ConvertOrder.crypt_id(order.id)
        return redirect('convert_order:files_main', order_id=encrypted_id)
    return render(request, 'convert_order/index.html', context)

def files_main(request, order_id):
    """ Главная страница с загруженныии файлыми."""
    logger.info('------files_main------')
    logger.info(f"request.POST: {request.POST}")
    logger.info(f"request.session: {request.session.items()}")
    logger.info(f'order_id = {order_id}')

    if request.session.get('back_to', None):
        request.session.pop('back_to')

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

