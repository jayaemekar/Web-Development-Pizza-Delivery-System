from django.urls import path
from . import views

urlpatterns = [
    path('user_login/', views.userLogin, name='login'),
    path('user_signup/', views.userReg, name='registration'),
    path('user_logout/', views.userLogout, name='logout'),
]