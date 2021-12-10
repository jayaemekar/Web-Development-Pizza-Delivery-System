from django.shortcuts import redirect

def stop_restaurant_staff(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_staff:
            return redirect('restaurant_admin:home_restaurant_staffs')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
