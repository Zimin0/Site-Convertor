from django.shortcuts import render, redirect, HttpResponse
from convert_order.models import ConvertOrder
from django.views.decorators.csrf import csrf_exempt

def payment_form(request):
    return render(request, 'payment/payment_form.html')

def load(request):
    return render(request, 'payment/load.html')


@csrf_exempt
def catch_payment(request):
    if request.method == 'GET':
        print(request.session.items())
        print(f"request.session['created_order_slug'] = {request.session['created_order_slug']}")
        created_order_slug = request.session['created_order_slug']
        order = ConvertOrder.objects.get(slug=created_order_slug)
        print(f"order.paid in GET = {order.paid}")
        if order.paid:
            return redirect('files:load_file', created_order_slug)
            return redirect('convert_order:files_main', created_order_slug)
        
        else:
            return HttpResponse("Shit in Modulbank!")
    
    if request.method == 'POST':
        print("Пришел POST запрос")
        post_data = request.POST
        response_text = "POST data:\n"

        for key, value in post_data.items():
            response_text += f"{key}: {value}\n"
        print(response_text)
        custom_order_id = request.POST['custom_order_id']

        print(f"request.POST['custom_order_id'] = {request.POST['custom_order_id']}")
        #request.session['back_to'] = custom_order_id
        order = ConvertOrder.objects.get(slug=custom_order_id)
        order.paid = True
        #request.session['custom_order_id'] = request.POST['custom_order_id']
        # order.modulbank_id = request.session['transaction_id']
        order.save()
        print(f"order.paid in POST = {order.paid}")
        return HttpResponse('ok')