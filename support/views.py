from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

from support.models import SupportRequest
from users.models import Profile
from production_settings.models import ProductionSettings


def support(request):
    """ Форма техподдрежки по кнопке на главной странице."""
    if not request.session.get('phone_is_confirmed', None):
        return redirect('users:login')
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
            formatted_message = f""" От {phone} \nПочта: {email} \nПриоритет: {priority} \nСообщение:\n{message} """
            # Отправляем письмо на почту техподдержки #
            msg = EmailMultiAlternatives(subject='Техподдержка', from_email=tech_mail, to=[email], body=formatted_message)
            status = msg.send()
            print(f"Статус отправки эл. письма на почту {email}: {status}")
            return redirect('convert_order:clear_main')
        else:
            return redirect('users:login')

    return render(request, 'support/support.html')

