from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from restaurant_admin.decorators import *
from restaurant_admin.forms import *
from pizza_home.models import *

# Create your views here.
# Home Page for restuarant admin
@login_required(login_url='userAuth:login')
@stop_regular_customer
def index(request):
    context = {}
    return render(request, 'restaurant_admin/index.html', context)

# Shows all the pizzas for restuarant admin
@login_required(login_url='userAuth:login')
@stop_regular_customer
def pizzaList(request):
    pizza_list = Pizza.objects.all()
    total_pizza_num = len(pizza_list)
    context = {
        'title': 'Pizza List',
        'pizzas': pizza_list,
        'total_pizza_num': total_pizza_num,
    }
    return render(request, 'restaurant_admin/pizza_menu_list.html', context)


# Create new pizza record for restaurant admin
@login_required(login_url='userAuth:login')
@stop_regular_customer
def createPizza(request):
    form = PizzaForm()

    if request.method == 'POST':
        form = PizzaForm(request.POST, request.FILES)  
        if form.is_valid():
            form.save()
            return redirect(request.get_full_path()) 

    context = {
        'title': 'New Pizza Record',
        'pizzaForm': form,
    }
    return render(request, 'restaurant_admin/pizza_record_create.html', context)


# Update pizza record for restaurant admin
@login_required(login_url='userAuth:login')
@stop_regular_customer
def updatePizza(request, pizza_id):
    pizza = Pizza.objects.filter(pk=pizza_id).first()
    form = PizzaForm(instance=pizza)

    if request.method == 'POST':
        form = PizzaForm(request.POST, request.FILES, instance=pizza)  
        if form.is_valid():
            form.save()
            return redirect('restaurant_admin:pizzaRecords') 
    context = {
        'title': 'Update Pizza Record',
        'pizza': pizza,
        'pizzaForm': form,
    }
    return render(request, 'restaurant_admin/pizza_record_update.html', context)


# Delete pizza record for restaurant admin
@login_required(login_url='userAuth:login')
@stop_regular_customer
def deletePizza(request, pizza_id):
    pizza = Pizza.objects.filter(pk=pizza_id).first()
    if request.method == 'POST':
        pizza.delete()
        return redirect('restaurant_admin:pizzaRecords')
    context = {
        'title': 'Restaurant Staffs: Delete Pizza Record',
        'pizza': pizza,
    }
    return render(request, 'restaurant_admin/pizza_record_delete.html', context)

# All orders-list for restaurant admin
@login_required(login_url='userAuth:login')
@stop_regular_customer
def restaurant_order_status_list(request):

    order = Order.objects.order_by('-id') 
    total_order_num = len(order)

    context = {
        'title': 'Restaurant Staff: Orders List',
        'orders': order,
        'total_order_num': total_order_num,
    }
    return render(request, 'restaurant_admin/order_status_list.html', context)


# Update order-status page for restaurant admin
@login_required(login_url='userAuth:login')
@stop_regular_customer
def restaurant_order_status_update(request, order_id):
    order = Order.objects.filter(order_id=order_id).first()
    order_user_full_name = order.user.first_name + ' ' + order.user.last_name
    print(order.user.first_name)
    print('%s %s' % (order.user.first_name, order.user.last_name))

    form = OrderStatusUpdateForm(instance=order)

    # If no such order with this order_id is found, redirect user to the home-page.
    if order is None:
        return redirect('restaurant_admin:restaurantBackendOrderStatus')

    if request.method == 'POST':
        form = OrderStatusUpdateForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect(request.get_full_path())    # redirect to the same page

    context = {
        'title': 'Restaurant Staff: Order Update',
        'order': order,
        'orderForm': form,
        'user_full_name': order_user_full_name,
    }
    return render(request, 'restaurant_admin/order_status_update.html', context)
