from django.contrib import admin
from .models import *

# Pizza-Admin Page
class PizzaAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at', 'price']
    search_fields = ['name']
    list_display_links = ['name']
    list_per_page = 15

admin.site.register(Pizza, PizzaAdmin)


# Oder-Admin Page
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'pizza', 'user', 'status', 'date', 'amount']
    list_filter = ['status']
    search_fields = ['order_id', 'status']
    list_display_links = ['order_id']
    list_per_page = 15

admin.site.register(Order, OrderAdmin)
