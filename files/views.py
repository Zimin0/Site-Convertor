from django.shortcuts import redirect, get_object_or_404, HttpResponse
from convert_order.models import ConvertOrder
from files.models import File
from django.http import FileResponse
from django.contrib.auth.models import User
from users.models import Profile

def load_file(request, order_id):
    """ При переходе сразу начинается скачивание файла. """

    decrypted_id = ConvertOrder.decrypt_id(order_id)
    order = get_object_or_404(ConvertOrder, id=decrypted_id)
    user_profile = get_object_or_404(Profile, phone=order.phone)
    user_profile.convert_already = True
    
    request.session['convert_already'] = user_profile.convert_already # переместить куда-то в другое место
    user_profile.save()

    # Формирование файла #
    file3 = get_object_or_404(File, order=order, file_type='3') # конвертированный файл
    filename = file3.file.name.split('/')[-1]
    response = FileResponse(file3.file.open('rb'))
    response.set_cookie('convert_already', True) # !!!!!!!!!!!!!!!!!!!!!!1
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
