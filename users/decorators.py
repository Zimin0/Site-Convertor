from django.shortcuts import redirect
from convert_order.models import ConvertOrder

def need_custom_login(func):
    """ Проверяет, вошел ли пользователь в аккаунт через проверку номера телефона. """
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('phone_is_confirmed', False):
            return redirect('users:login')
        return func(request, *args, **kwargs)
    return _wrapped_view

def alredy_custom_logined(func):
    """ Если пользователь вошел в аккаунт через номер телефона, перенаправляет на страницу "Телефон подтвержден!". """
    def _wrapped_view(request, *args, **kwargs):
        if request.session.get('phone_is_confirmed', False):
            return redirect('users:good_code')
        return func(request, *args, **kwargs)
    return _wrapped_view

def log_veriables(func):
    """ Выводит на экран содержимое session, GET, POST, переменные, переданные в функцию"""
    def wrapper(request, *args, **kwargs):
        func_name = func.__name__
        print(f'----------{func_name}----------')
        print(f'------------ARGUMENTS------------')
        arguments_string = ''
        for variable in kwargs.items():
            arguments_string += f""""{variable[0]}":{variable[1]}\n"""
        print(arguments_string[:-1]) if len(arguments_string) > 0 else None
        print(f'-------------SESSION-------------')
        session_string = ''
        for variable in request.session.items():
            session_string += f""""{variable[0]}":{variable[1]}\n"""
        print(session_string[:-1]) if len(session_string) > 0 else None # обрезает последний \n
        print(f'--------------POST---------------')
        post_string = ''
        for variable in request.POST.items():
            post_string += f""""{variable[0]}":{variable[1]}\n"""
        print(post_string[:-1]) if len(post_string) > 0 else None
        print(f'---------------GET---------------')
        get_string = ''
        for variable in request.GET.items():
            get_string += f""""{variable[0]}":{variable[1]}\n"""
        print(get_string[:-1]) if len(get_string) > 0 else None
        print('----------------------------------') 
        return func(request, *args, **kwargs)
    return wrapper

def can_back_to_download(func):
    """ Позволяет вернуться с ~любой страницы на страницу скачивание конвертированного файла """
    def wrapper(request, *args, **kwargs):
        if request.session.get('created_order_slug', False):
            request.session['need_to_back_to_download'] = True
        # context["need_to_back"] = request.session.get('need_to_back_to_download', False)
        # if context["need_to_back"]:
        #     context['order_id'] = ConvertOrder.decrypt_id(request.session.get('created_order_slug', False))
        return func(request, *args, **kwargs)
    return wrapper