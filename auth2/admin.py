from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User


class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'code', 'imageURI')}),
        (_('Permissions'), {
            'fields': ('is_verified', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'), # 'session_id', 
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_filter = ('is_staff', 'is_active', 'is_verified')
    list_display = ('username', 'email', 'is_active', 'is_staff', 'is_verified', 'date_joined')


admin.site.register(User, UserAdmin)