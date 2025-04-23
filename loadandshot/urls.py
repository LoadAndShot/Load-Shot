"""
URL configuration for Load&Shot project.
Inclut les routes de l'application principale 'orders' et l'interface d'administration.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('orders.urls')),  # inclure les URLs de l'application orders
]
