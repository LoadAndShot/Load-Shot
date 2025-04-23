# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.contrib import messages

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

    actions = ['unlock_catalogues_for_all', 'lock_catalogues_for_all']

    @admin.action(description="✅ Déverrouiller l'accès aux 2 catalogues pour tout le monde")
    def unlock_catalogues_for_all(self, request, queryset):
        updated = CustomUser.objects.update(can_access_catalogue1=True, can_access_catalogue2=True)
        self.message_user(request, f"L'accès aux catalogues a été déverrouillé pour {updated} utilisateurs.", messages.SUCCESS)

    @admin.action(description="🔒 Verrouiller l'accès aux 2 catalogues pour tout le monde")
    def lock_catalogues_for_all(self, request, queryset):
        updated = CustomUser.objects.update(can_access_catalogue1=False, can_access_catalogue2=False)
        self.message_user(request, f"L'accès aux catalogues a été verrouillé pour {updated} utilisateurs.", messages.WARNING)
