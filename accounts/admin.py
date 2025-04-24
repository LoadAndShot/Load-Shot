from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'can_access_catalogue1', 'can_access_catalogue2')
    list_filter = ('is_staff', 'is_superuser', 'can_access_catalogue1', 'can_access_catalogue2')
    search_fields = ('username', 'email')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password', 'email', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'can_access_catalogue1', 'can_access_catalogue2')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
    )
    actions = ['unlock_catalogue1_for_all', 'lock_catalogue1_for_all', 'unlock_catalogue2_for_all', 'lock_catalogue2_for_all']

    @admin.action(description='Déverrouiller Catalogue 1 pour TOUS les utilisateurs')
    def unlock_catalogue1_for_all(self, request, queryset):
        CustomUser.objects.update(can_access_catalogue1=True)
        self.message_user(request, "Catalogue 1 déverrouillé pour tous les utilisateurs.")

    @admin.action(description='Verrouiller Catalogue 1 pour TOUS les utilisateurs')
    def lock_catalogue1_for_all(self, request, queryset):
        CustomUser.objects.update(can_access_catalogue1=False)
        self.message_user(request, "Catalogue 1 verrouillé pour tous les utilisateurs.")

    @admin.action(description='Déverrouiller Catalogue 2 pour TOUS les utilisateurs')
    def unlock_catalogue2_for_all(self, request, queryset):
        CustomUser.objects.update(can_access_catalogue2=True)
        self.message_user(request, "Catalogue 2 déverrouillé pour tous les utilisateurs.")

    @admin.action(description='Verrouiller Catalogue 2 pour TOUS les utilisateurs')
    def lock_catalogue2_for_all(self, request, queryset):
        CustomUser.objects.update(can_access_catalogue2=False)
        self.message_user(request, "Catalogue 2 verrouillé pour tous les utilisateurs.")
