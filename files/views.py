from django.shortcuts import redirect, get_object_or_404, HttpResponse
from convert_order.models import ConvertOrder
from files.models import File
from django.http import FileResponse

def load_file(request, order_id):
    """ При переходе сразу начинается скачивание файла. """
    context = {}
    decrypted_id = ConvertOrder.decrypt_id(order_id)
    order = get_object_or_404(ConvertOrder, id=decrypted_id) # Оптимизировать запрос
    file3 = get_object_or_404(File, order=order, file_type='3') # конвертированный файл
    response = FileResponse(file3.file.open('rb'))
    response['Content-Disposition'] = 'attachment; filename="%s"' % file3.file.name
    return response
