# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import redirect, get_object_or_404, HttpResponse
from convert_order.models import ConvertOrder
from files.models import File as MyFile
from django.http import FileResponse
from users.models import Profile

def load_file(request, order_id):
    """ При переходе сразу начинается скачивание файла. """

    decrypted_id = ConvertOrder.decrypt_id(order_id)
    order = get_object_or_404(ConvertOrder, id=decrypted_id)
    user_profile = get_object_or_404(Profile, phone=order.phone)
    user_profile.convert_already = True 
    if user_profile.amount_of_converts > 0:
        user_profile.amount_of_converts -= 1
    else:
        raise ValueError()
    user_profile.save()

    # Заполняем сессию данными
    request.session['convert_already'] = user_profile.convert_already
    # Формирование файла #
    file3 = get_object_or_404(MyFile, order=order, file_type='3') # конвертированный файл
    filename = file3.file.name.split('/')[-1]

    # Открываем файл в режиме двоичного чтения и декодируем его из UTF-16, игнорируя ошибки
    print('path to result file =', file3.file.path)
    with open(file3.file.path, 'rb') as file:
        binary_content = file.read()
        #print(binary_content)
        content_utf16 = binary_content.decode('utf-8', errors='ignore')

    # Возвращаем содержимое файла в ответе с указанием кодировки UTF-16
    response = HttpResponse(content_utf16, content_type='application/xml; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response
