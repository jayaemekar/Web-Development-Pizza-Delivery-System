from django.shortcuts import redirect


def stop_regular_customer(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('pizza_home:homepage')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
