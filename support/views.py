from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

from support.models import SupportRequest
from users.models import Profile
from production_settings.models import ProductionSettings


def support(request):
    """ Форма техподдрежки по кнопке на главной странице."""
    if request.method == 'POST':
        if request.session.get('phone', False):
            phone = request.session['phone']
            print('phone =', phone)
            email = request.POST['email']
            priority = request.POST['priority']
            message = request.POST['message']
            user = get_object_or_404(Profile, phone=phone).user
            SupportRequest.objects.create(
                user=user,
                phone=phone,
                email=email,
                priority_rate = priority,
                message=message
            )
            tech_mail = get_object_or_404(ProductionSettings, slug='TECH_EMAIL') # почта тех. поддержки
            formatted_message = f""" От {phone}. \nПочта: {email} \nПриоритет: {priority} \nСообщение:\n{message} """
            
            msg = EmailMultiAlternatives(subject='Техподдержка', to=['nikzim2004@gmail.com'])
            msg.send()
            # send_mail(
            #     'Техподдержка сайта SAP XML Converter',
            #     formatted_message,
            #     'zimi3056@gmail.com',
            #     [email],
            #     fail_silently=False,
            # )
            return redirect('convert_order:clear_main')
        else:
            return redirect('user:login')

    return render(request, 'support/support.html')

