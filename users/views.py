from django.shortcuts import render, redirect, get_object_or_404

from convert_order.models import ConvertOrder
def phone(request, order_id):
    """ Страница с формой ввода номера телефона. """

    context = {}

    if request.method == 'POST':
        request.session['phone'] = request.POST['phone']
        # if request.user.profile.convert_already: # уже конвертировал на этом сайте
        #     redirect('payment:payment')
        decrypted_id = ConvertOrder.decrypt_id(order_id)
        order = get_object_or_404(ConvertOrder, id=decrypted_id) 
        return redirect('convert_order:download_file_page', order_id=order.id) 
    return render(request, 'users/phone.html', context)
