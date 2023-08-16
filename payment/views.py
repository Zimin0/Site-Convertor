from django.shortcuts import render, HttpResponse

def payment_form(request):
    return render(request, 'payment/payment_form.html')

def catch_payment(request):
    print("Пойман запрос о проведенной успешной оплате")
    print(request.GET)
    print(request.POST)
    return HttpResponse('ok')