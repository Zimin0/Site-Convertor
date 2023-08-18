from django.shortcuts import render, redirect, HttpResponse
from convert_order.models import ConvertOrder
from django.views.decorators.csrf import csrf_exempt
from users.decorators import log_veriables

def payment_form(request):
    return render(request, 'payment/payment_form.html')

def load(request):
    return render(request, 'payment/load.html')

@csrf_exempt
@log_veriables
def catch_payment(request):
    if request.method == 'GET':
        print(f"request.session.get('created_order_slug', False) = ", request.session.get('created_order_slug', False) )
        created_order_slug = request.session.get('created_order_slug', False)
        print('created_order_slug =', created_order_slug)
        order = ConvertOrder.objects.get(slug=created_order_slug)
        print(f"order.slug= ", order.slug)
        if order.paid:
            return render(request, 'payment/payment_success.html', {'order_id': order.slug})
        else:
            # добавить счетчик 3 перезагрузок 
            # return render(request, 'payment/payment_error.html')
            return redirect("payment:load")
    
    if request.method == 'POST':
        if request.POST['state'] == 'COMPLETE':
            custom_order_id = request.POST['custom_order_id']
            order = ConvertOrder.objects.get(slug=custom_order_id)
            order.paid = True
            order.save()
        else:
            print('Some error in modulbank appeared!')
        return HttpResponse('ok')