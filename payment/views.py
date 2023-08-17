from django.shortcuts import render, redirect, HttpResponse
from convert_order.models import ConvertOrder
from django.views.decorators.csrf import csrf_exempt
from users.decorators import log_veriables

def payment_form(request):
    return render(request, 'payment/payment_form.html')

def load(request):
    return render(request, 'payment/load.html')

@log_veriables
@csrf_exempt
def catch_payment(request):
    if request.method == 'GET':
        created_order_slug = request.session['created_order_slug']
        order = ConvertOrder.objects.get(slug=created_order_slug)
        if order.paid:
            return redirect('files:load_file', created_order_slug)
        else:
            return HttpResponse("Shit in Modulbank!")
    
    if request.method == 'POST':
        order = ConvertOrder.objects.get(slug=custom_order_id)
        order.paid = True
        #request.session['custom_order_id'] = request.POST['custom_order_id']
        # order.modulbank_id = request.session['transaction_id']
        order.save()
        print(f"order.paid in POST = {order.paid}")
        return HttpResponse('ok')