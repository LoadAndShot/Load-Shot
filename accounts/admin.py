from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'can_access_catalogue1', 'can_access_catalogue2', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'can_access_catalogue1', 'can_access_catalogue2')
    search_fields = ('username', 'email')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'phone_number')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Catalogue Access'), {'fields': ('can_access_catalogue1', 'can_access_catalogue2')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'phone_number', 'can_access_catalogue1', 'can_access_catalogue2', 'is_staff', 'is_active')}
        ),
    )

    actions = ['unlock_catalogue1', 'lock_catalogue1', 'unlock_catalogue2', 'lock_catalogue2']

    @admin.action(description="Déverrouiller l'accès au Catalogue 1 pour tous les utilisateurs")
    def unlock_catalogue1(self, request, queryset):
        CustomUser.objects.update(can_access_catalogue1=True)

    @admin.action(description="Verrouiller l'accès au Catalogue 1 pour tous les utilisateurs")
    def lock_catalogue1(self, request, queryset):
        CustomUser.objects.update(can_access_catalogue1=False)

    @admin.action(description="Déverrouiller l'accès au Catalogue 2 pour tous les utilisateurs")
    def unlock_catalogue2(self, request, queryset):
        CustomUser.objects.update(can_access_catalogue2=True)

    @admin.action(description="Verrouiller l'accès au Catalogue 2 pour tous les utilisateurs")
    def lock_catalogue2(self, request, queryset):
        CustomUser.objects.update(can_access_catalogue2=False)
