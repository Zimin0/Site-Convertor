from django.shortcuts import render, HttpResponse
from convert_order.models import ConvertOrder


def show_order(request):
    order = ConvertOrder.objects.first()
    return HttpResponse(order.get_formatted_creation_date())