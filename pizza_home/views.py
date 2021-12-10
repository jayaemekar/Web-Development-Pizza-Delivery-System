from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .decorators import *
from .models import *

@login_required(login_url='userAuth:login')
@stop_restaurant_staff
def index(request):
    try:
        user = request.user    
        user = user.get_full_name()  
    except:
        user = 'Anonymous User'

    pizza = Pizza.objects.all()
    total_pizza_num = len(pizza)
    pizza_paginator = Paginator(pizza, 4)
    pizza_page = request.GET.get('page')
    paginated_pizza_list_query = pizza_paginator.get_page(pizza_page)

    context = {
        'title': 'Cal Pizza Delivery System',     
        'user': user,
        'pizzas': paginated_pizza_list_query,
        'total_pizza_num': total_pizza_num,
    }
    return render(request, 'pizza_home/index.html', context)

@login_required(login_url='userAuth:login')
@stop_restaurant_staff
def order(request, order_id):
    try:
        user = request.user  
        user = user.get_full_name() 
    except:
        user = 'Anonymous User'
    order = Order.objects.filter(order_id=order_id).first()
    if order is None:
        return redirect('pizza_home:homepage')
    context = {
        'title': 'Pizza App: Order Status Page',
        'order': order,
        'user': user,
    }
    return render(request, 'pizza_home/order.html', context)

@login_required(login_url='userAuth:login')
@stop_restaurant_staff
def order_list(request):
    try:
        user = request.user 
        user = user.get_full_name()
    except:
        user = 'Anonymous User'

    order = Order.objects.order_by('-id').filter(user_id=request.user.id)   # display the latest orders
    total_order_num = len(order)
    order_paginator = Paginator(order, 5)
    order_page = request.GET.get('page')
    paginated_order_list_query = order_paginator.get_page(order_page)
    context = {
        'title': 'Orders List',
        'user': user,
        'orders': paginated_order_list_query,
        'total_order_num': total_order_num,
    }

    return render(request, 'pizza_home/order_list.html', context)



def error_404_view(request, exception):
    return render(request, '404_page_not_found.html')

@login_required(login_url='userAuth:login')
@stop_restaurant_staff
def room(request):
    try:
        user = request.user
        user = user.get_full_name()
    except:
        user = 'Anonymous User'
    context = {
        'user': user,
    }
    return render(request, 'pizza_home/room.html', context)

def about_view(request):
    try:
        user = request.user
        user = user.get_full_name()
    except:
        user = 'Anonymous User'

    context = {
        'user': user,
    }
    return render(request , 'pizza_home/about.html',context)


def contactus_view(request):
    try:
        user = request.user
        user = user.get_full_name()
    except:
        user = 'Anonymous User'

    context = {
        'user': user,
    }
    return render(request , 'pizza_home/contactus.html',context)

@login_required(login_url='userAuth:login')
@stop_restaurant_staff
def show_pizza_record(request,name):
    try:
        user = request.user
        user = user.get_full_name()
    except:
        user = 'Anonymous User'

    pizza = Pizza.objects.filter(name=name).first()
    context = {
        'user': user,
        'pizza': pizza,
        'name': name,
    }
    return render(request , 'pizza_home/show_pizza_record.html',context)

@csrf_exempt
@stop_restaurant_staff
def order_pizza(request):
    # return JsonResponse({ 'testing': 'Success' }) # testing API

    try:
        print("Test",request.user)
        print(json.loads(request.body))
        
        # fetching data send from the frontend func ("createOrder")
        user = request.user # fetch user info from 'index.html'
      
        data = json.loads(request.body) # fetch all the django-vars from 'index.html', especially focuses on 'pizza' information. Converts a JSON-obj to a python-dictionary.
        
        print("Test",user)
        pizza = Pizza.objects.get(id=data.get('id'))    # extract the specific pizza-obj from db using the 'pizza.id' onclick 'createOrder({{p.id}})' func existed in 'index.html'
        
        # [ INSERT RECORD TO DB ]
        # Creating an single-record in the 'Order' model-class
        order = Order(user=user, pizza=pizza, amount=pizza.price)
        order.save()

        return JsonResponse({ 'status': True, 'message': 'Success', 'order': 'A new order is created' })
    except:
        return JsonResponse({ 'status': False, 'error': 'Something went wrong' })
