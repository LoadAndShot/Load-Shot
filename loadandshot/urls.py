from django.contrib import admin
from django.urls import path, include  # ✅ N'oublie pas 'include' !

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('orders.urls')),  # ✅ On inclut les routes de l'app 'orders'
]

