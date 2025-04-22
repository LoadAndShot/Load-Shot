from django.contrib import admin
from django.urls import path
from orders import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('order/', views.create_order_view, name='create_order'),
    path('', views.home_view, name='home'),
    path('test/', views.test_view, name='test'),  # 🔥 Page de test CSS
]
