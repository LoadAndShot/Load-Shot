# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Définir les champs visibles dans les sections de l'admin
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

    # Champs pour l'ajout d'un nouvel utilisateur (affiche can_access_catalogue1/2 même à la création)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'phone_number', 'can_access_catalogue1', 'can_access_catalogue2', 'is_staff', 'is_active')}
        ),
    )

    # Colonnes affichées dans la liste des utilisateurs
    list_display = ('username', 'email', 'is_staff', 'can_access_catalogue1', 'can_access_catalogue2')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'can_access_catalogue1', 'can_access_catalogue2', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
