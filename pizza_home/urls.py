from django.urls import path, include
from . import views

app_name = 'homeApp'

urlpatterns = [
    path('', views.index, name='homepage'),
    path('order_list/', views.order_list, name='order_list'),
    path('api/order/', views.order_pizza),
    path('order/<str:order_id>/', views.order, name='order'),
    path('chatroom/', views.room, name='room'),
    path('chatroom/chat/', views.room, name='room'),
    path('about/', views.about_view, name='about'),
    path('contactus/', views.contactus_view, name='contactus_view'),
    path('show_pizza_record/<str:name>/', views.show_pizza_record, name='show_pizza_record'),
]