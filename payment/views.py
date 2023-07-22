from django.shortcuts import render, HttpResponse

def payment(request):
    return HttpResponse('<h1>Payment</h1>')
