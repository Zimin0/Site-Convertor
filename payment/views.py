from django.shortcuts import render

def payment_form(request):
    return render(request, 'payment/payment_form.html')
