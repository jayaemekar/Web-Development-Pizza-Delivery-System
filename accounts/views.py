from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm
from .decorators import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout,authenticate

@stop_authenticated_users
def userLogin(request):
    context = {'title': 'User Login', }
    form = UserLoginForm()
    context['loginForm'] = UserLoginForm()

    if request.POST:
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser or user.is_admin or user.is_staff:
                    return redirect('restaurant_admin:home_restaurant_staffs')
                else:
                    return redirect('pizza_home:homepage')

        messages.info(request, 'Invalid Credentials!')
        return redirect('userAuth:login')

    return render(request, 'accounts/loginForm.html', context)


@stop_authenticated_users
def userReg(request):
    context = { 'title': 'User Registration', }
 
    if request.POST:
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('userAuth:login')
        else:
            context['registerForm'] = form
    else:
        form = UserRegistrationForm() 
        context['registerForm'] = form
          
    return render(request, 'accounts/regForm.html', context)

@login_required(login_url='userAuth:login')
def userLogout(request):
    logout(request)
    return redirect('userAuth:login')
