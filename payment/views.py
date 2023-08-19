from django.shortcuts import render, redirect, HttpResponse
from convert_order.models import ConvertOrder
from django.views.decorators.csrf import csrf_exempt
from users.decorators import log_veriables

import json

def payment_form(request):
    return render(request, 'payment/payment_form.html')

def load(request):
    return render(request, 'payment/load.html')

@csrf_exempt
@log_veriables
def catch_payment(request):
    if request.method == 'GET':
        created_order_slug = request.session.get('created_order_slug', False)
        order = ConvertOrder.objects.get(slug=created_order_slug)
        if order.paid:
            request.session.pop('times_of_waiting', False) 
            return render(request, 'payment/payment_success.html', {'order_id': order.slug})
        else:
            times = request.session.get('times_of_waiting', False)
            error_in_payment = request.session.get('error_in_payment', False)
            if error_in_payment:
                return render(request, 'payment/payment_error.html', {'order_id': order.slug})
            if times:
                if times > 2:
                    request.session.pop('times_of_waiting', False) 
                    request.session['error_in_payment'] = True
                    return render(request, 'payment/payment_error.html', {'order_id': order.slug})
                request.session['times_of_waiting'] += 1
            else:
                request.session['times_of_waiting'] = 0
            
            return redirect('payment:load')
    
    if request.method == 'POST':
        if request.POST['state'] == 'COMPLETE':
            custom_order_id = request.POST['custom_order_id']
            order = ConvertOrder.objects.get(slug=custom_order_id)
            order.paid = True 
            order.price = float(request.POST['original_amount'])
            order.modulbank_transaction_id = json.loads(request.POST['meta'])['bill_id']
            order.save()
        else:
            print('Some error in modulbank appeared!')
        return HttpResponse('ok')