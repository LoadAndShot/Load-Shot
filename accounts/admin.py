from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'can_access_catalogue1', 'can_access_catalogue2')
    list_filter = ('is_staff', 'can_access_catalogue1', 'can_access_catalogue2')
    ordering = ('username',)

    change_list_template = "admin/customuser_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('unlock_catalogue1/', self.admin_site.admin_view(self.unlock_catalogue1), name='unlock_catalogue1'),
            path('lock_catalogue1/', self.admin_site.admin_view(self.lock_catalogue1), name='lock_catalogue1'),
            path('unlock_catalogue2/', self.admin_site.admin_view(self.unlock_catalogue2), name='unlock_catalogue2'),
            path('lock_catalogue2/', self.admin_site.admin_view(self.lock_catalogue2), name='lock_catalogue2'),
        ]
        return custom_urls + urls

    def unlock_catalogue1(self, request):
        CustomUser.objects.update(can_access_catalogue1=True)
        self.message_user(request, "✅ Catalogue 1 (Légal) déverrouillé pour tous les utilisateurs.", messages.SUCCESS)
        return redirect("admin:accounts_customuser_changelist")

    def lock_catalogue1(self, request):
        CustomUser.objects.update(can_access_catalogue1=False)
        self.message_user(request, "🔒 Catalogue 1 (Légal) verrouillé pour tous les utilisateurs.", messages.WARNING)
        return redirect("admin:accounts_customuser_changelist")

    def unlock_catalogue2(self, request):
        CustomUser.objects.update(can_access_catalogue2=True)
        self.message_user(request, "✅ Catalogue 2 (Spécial) déverrouillé pour tous les utilisateurs.", messages.SUCCESS)
        return redirect("admin:accounts_customuser_changelist")

    def lock_catalogue2(self, request):
        CustomUser.objects.update(can_access_catalogue2=False)
        self.message_user(request, "🔒 Catalogue 2 (Spécial) verrouillé pour tous les utilisateurs.", messages.WARNING)
        return redirect("admin:accounts_customuser_changelist")
