from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from convert_order.models import ConvertOrder
from django.http import HttpResponse
from files.models import File


def orders(request):
    """ Отображает все сделанные заказы на конвертацию. """
    order = ConvertOrder.objects.first()
    if order is not None:
        return HttpResponse(order.get_formatted_creation_date())
    else:
        return HttpResponse("Заказов нет!")


def converter(request):
    """ Отображает страницу для загрузки файлов. """
    context = {}
    print(request.POST)
    
    if request.method == 'POST':
        if len(request.FILES) < 2: # если загружено меньше, чем 2 файла
            context['message'] = 'Загрузите оба файла!'
            return render(request, 'convert_order/main_convert.html', context)
        
        file1 = request.FILES['file1']
        file2 = request.FILES['file2']
        print(file1, file2)
        context['message'] = f'Файлы {file1.name} и {file2.name} загружены!'
        
        # Создаем новый заказ на конвертацию и добавляем файлы #
        order = ConvertOrder(user=request.user)
        order.save()
        File.objects.create(order=order , file=file1, file_type='1').save()
        File.objects.create(order=order, file=file2, file_type='2').save()
        ########################################################

        encrypted_id = ConvertOrder.crypt_id(order.id)
        return redirect('convert_order:download_file_page', order_id=encrypted_id)
        #return redirect('users:phone', order_id=encrypted_id)
    
    return render(request, 'convert_order/main_convert.html', context)


def download_file_page(request, order_id):
    """ Страница для скачивания сконвертированного файла. Получает на вход id заказа конвертации."""

    context = {}
    context["order_id"] = order_id
    return render(request, 'convert_order/main_with_download.html', context)

def download_file(request, order_id):
    """ При переходе сразу начинается скачивание файла. """

    context = {}

    decrypted_id = ConvertOrder.decrypt_id(order_id)

    order = get_object_or_404(ConvertOrder, id=decrypted_id) # Оптимизировать запрос
    file3 = get_object_or_404(File, order=order, file_type='3') # конвертированный файл. Проверка на тип - для надежности

    context['file3'] = file3
    filename = file3.file.name.split('/')[-1]
    response = HttpResponse(file3.file, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response
