from django.shortcuts import redirect, get_object_or_404, HttpResponse
from convert_order.models import ConvertOrder
from files.models import File

def load_file(request, order_id):
    """ При переходе сразу начинается скачивание файла. """

    context = {}

    if not request.session['phone_confirmed']: # если вдруг юзер добрался до этой страницы, а телефон не подтвержден
        return redirect('convert_order:phone_main', order_id)

    decrypted_id = ConvertOrder.decrypt_id(order_id)

    order = get_object_or_404(ConvertOrder, id=decrypted_id) # Оптимизировать запрос
    file3 = get_object_or_404(File, order=order, file_type='3') # конвертированный файл. Проверка на тип - для надежности

    context['file3'] = file3
    filename = file3.file.name.split('/')[-1]
    response = HttpResponse(file3.file, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response
