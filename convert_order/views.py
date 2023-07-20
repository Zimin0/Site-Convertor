from django.shortcuts import render, redirect, HttpResponse
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
    
    if request.method == 'POST':
        if len(request.FILES) < 2: # если загружено меньше, чем 2 файла
            context['message'] = 'Загрузите оба файла!'
            return render(request, 'convert_order/main_convert.html', context)
        
        file1 = request.FILES['file1']
        file2 = request.FILES['file2']
        print(file1, file2)

        context['message'] = f'Файлы {file1.name} и {file2.name} загружены!'

        order = ConvertOrder(user=request.user)
        order.save()

        # Создаем новый заказ на конвертацию и добавляем файлы
        File.objects.create(order=order , file=file1, file_type='1').save()
        File.objects.create(order=order, file=file2, file_type='2').save()
        # request.session['order_id'] = order.id
        return redirect('users:phone', order_id=order.id)
    
    return render(request, 'convert_order/main_convert.html', context)


def download_file(request, order_id):
    """ Страница для скачивания сконвертированного файла. Получает на вход id заказа конвертации."""
    return HttpResponse('done!!!')