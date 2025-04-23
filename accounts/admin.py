from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Informations personnelles'), {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Accès Catalogues'), {
            'fields': ('can_access_catalogue1', 'can_access_catalogue2'),
        }),
        (_('Dates importantes'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'phone_number', 'can_access_catalogue1', 'can_access_catalogue2', 'is_staff', 'is_active')}
        ),
    )

    list_display = ('username', 'email', 'is_staff', 'can_access_catalogue1', 'can_access_catalogue2')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'can_access_catalogue1', 'can_access_catalogue2', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    change_list_template = "admin/accounts/customuser/change_list.html"  # Custom template

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('unlock_catalogues/', self.admin_site.admin_view(self.unlock_catalogues), name='unlock_catalogues'),
            path('lock_catalogues/', self.admin_site.admin_view(self.lock_catalogues), name='lock_catalogues'),
        ]
        return custom_urls + urls

    def unlock_catalogues(self, request):
        CustomUser.objects.update(can_access_catalogue1=True, can_access_catalogue2=True)
        self.message_user(request, "✅ Tous les catalogues ont été déverrouillés pour tous les utilisateurs.", messages.SUCCESS)
        return redirect('..')

    def lock_catalogues(self, request):
        CustomUser.objects.update(can_access_catalogue1=False, can_access_catalogue2=False)
        self.message_user(request, "🔒 Tous les catalogues ont été verrouillés pour tous les utilisateurs.", messages.WARNING)
        return redirect('..')
