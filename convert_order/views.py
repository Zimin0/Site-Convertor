from django.shortcuts import render, HttpResponse
from convert_order.models import ConvertOrder
from django.http import HttpResponse


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
        file1 = request.FILES['file1']
        file2 = request.FILES['file2']

        context['message'] = f'Файлы {file1.name} и {file2.name} загружены!'

        # Создаем новый заказ на конвертацию
        order = ConvertOrder(user=request.user)
        order.save()

    return render(request, 'main_convert.html', context)
