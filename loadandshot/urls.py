from django.contrib import admin
from django.urls import path, include
from orders import views  # 🟢 Import de la vue accueil

urlpatterns = [
    path('', views.home_view, name='home'),  # 🟢 Page d'accueil
    path('admin/', admin.site.urls),
    path('', include('orders.urls')),       # 🟢 Les autres routes (login, register, etc.)
]
