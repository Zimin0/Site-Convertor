from django.shortcuts import render, redirect, HttpResponse

def phone(request, order_id):
    context = {}

    if request.method == 'POST':
        phone = request.POST['phone']
        return redirect('convert_order:download_file_page', order_id=order_id)
    return render(request, 'users/phone.html', context)
