from django.urls import path
from . import views  # ✅ On importe les vues de ton app

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('order/', views.create_order_view, name='create_order'),  # 🟥 C'est bien là que la vue doit être reliée
    path('test/', views.test_view, name='test'),
]
