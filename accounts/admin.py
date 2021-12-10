from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class CustomUserAdmin(BaseUserAdmin):
    list_display = ['email', 'company_name', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_active', 'is_staff', 'is_admin', 'is_superuser']
    list_display_links = ['email']
    search_fields = ['email', 'company_name', 'first_name', 'last_name', 'phone']
    readonly_fields = ['date_joined', 'last_login'] # to view these fields in the user-detail page inside the admin-panel
    filter_horizontal = []
    fieldsets = []
    list_filter = ['last_login']
    list_per_page = 15
    ordering = ['email']

    add_fieldsets = [
        (None, {
            'classes':('wide'),
            'fields':('email', 'company_name', 'phone', 'password1', 'password2'),
        })
    ]

admin.site.register(CustomUser, CustomUserAdmin)