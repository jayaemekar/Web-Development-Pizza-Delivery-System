from . import views
from django.urls import path
app_name = 'restaurantStaffApp'

urlpatterns = [
    path('', views.index, name='home_restaurant_staffs'),
    path('order-list/', views.restaurant_order_status_list, name='restaurantBackendOrderStatus'),
    path('pizza/pizza-records/', views.pizzaList, name='pizzaRecords'),
    path('pizza/create-pizza-record/', views.createPizza, name='createPizzaRecord'),
    path('pizza/delete-pizza-record/<str:pizza_id>/', views.deletePizza, name='deletePizzaRecord'),
    path('pizza/update-pizza-record/<str:pizza_id>/', views.updatePizza, name='updatePizzaRecord'),
    path('order-status-update/<str:order_id>/', views.restaurant_order_status_update, name='orderStatusUpdate'),
]