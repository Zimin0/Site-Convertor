from django.shortcuts import render, redirect
from convert_order.models import ConvertOrder
from files.models import File


def clear_main(request):
    """ Отображает страницу для загрузки файлов. """
    context = {}
    print(request.POST)
    
    if request.method == 'POST':
        if len(request.FILES) < 2: # если загружено меньше, чем 2 файла
            context['message'] = 'Загрузите оба файла!'
            return render(request, 'convert_order/index.html', context)
        
        file1 = request.FILES['file1']
        file2 = request.FILES['file2']
        print(file1, file2)
        context['message'] = f'Файлы {file1.name} и {file2.name} загружены!'
        
        # Создаем новый заказ на конвертацию и добавляем файлы #
        order = ConvertOrder() 
        order.save() 
        File.objects.create(order=order , file=file1, file_type='1').save()
        File.objects.create(order=order, file=file2, file_type='2').save()
        ########################################################

        encrypted_id = ConvertOrder.crypt_id(order.id)
        request.session['phone_confirmed'] = False
        request.session['phone'] = ''
        return redirect('convert_order:phone_main', order_id=encrypted_id)

    return render(request, 'convert_order/index.html', context)

def phone_main(request, order_id):
    """ Главная страница с переданным order_id"""
    context = {}

    phone_confirmed = request.session['phone_confirmed']
    context['phone_confirmed'] = phone_confirmed
    context['phone'] = request.session['phone']
    context['order_id'] = order_id
    if phone_confirmed:
        decrypted_id = ConvertOrder.decrypt_id(order_id)
        context['order_id'] = decrypted_id


    return render(request, 'convert_order/index.html', context) 



