from django.shortcuts import redirect

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
    """ Выводит на экран содержимое session, GET, POST. """
    def wrapper(request, *args, **kwargs):
        func_name = func.__name__
        print(f'----------{func_name}----------')
        print(f'-------------SESSION-------------')
        session_string = ''
        for variable in request.session.items():
            session_string += f""""{variable[0]}":{variable[1]}\n"""
        print(session_string[:-2]) if len(session_string) > 0 else None # обрезает последний \n
        print(f'--------------POST---------------')
        post_string = ''
        for variable in request.POST.items():
            post_string += f""""{variable[0]}":{variable[1]}\n"""
        print(post_string[:-2]) if len(post_string) > 0 else None
        print(f'---------------GET---------------')
        get_string = ''
        for variable in request.GET.items():
            get_string += f""""{variable[0]}":{variable[1]}\n"""
        print(get_string[:-2]) if len(get_string) > 0 else None
        print('----------------------------------') 
        return func(request, *args, **kwargs)
    return wrapper

def can_back_to_download():
    """ Позволяет вернуться с ~любой страницы на страницу скачивание конвертированного файла """
    pass 