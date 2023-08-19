from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User

from support.models import SupportRequest
from users.models import Profile
from production_settings.models import ProductionSettings
from users.decorators import need_custom_login

@need_custom_login
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
            profile = get_object_or_404(Profile, phone=phone) ## Заносим в БД почту, введенную в окне поддержки ##
            profile.user.email = email 
            profile.user.save(update_fields=['email',])
            ## Подтягиваем настройку почты тех.поддержки из админки ##
            tech_mail = get_object_or_404(ProductionSettings, slug='TECH_EMAIL_FROM') # почта тех. поддержки
            
            formatted_message = f""" От {phone} \nПочта: {email} \nПриоритет: {priority} \nСообщение:\n{message} """
            # Отправляем письмо на почту техподдержки #
            msg = EmailMultiAlternatives(subject='Техподдержка', from_email=tech_mail, to=[email], body=formatted_message)
            status = msg.send() # GMAIL_APP_KEY
            print(f"Статус отправки эл. письма на почту {email}: {status}")
            return redirect('convert_order:clear_main')
        else:
            return redirect('users:login')

    return render(request, 'support/support.html')

