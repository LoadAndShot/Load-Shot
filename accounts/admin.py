from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_locked_catalogue1', 'is_locked_catalogue2')
    fieldsets = UserAdmin.fieldsets + (
        ('Catalogue Locks', {'fields': ('is_locked_catalogue1', 'is_locked_catalogue2')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

