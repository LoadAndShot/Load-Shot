# commands/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # Vue principale après connexion
    path('catalogue1/', views.catalogue1, name='catalogue1'),
    path('catalogue2/', views.catalogue2, name='catalogue2'),
    path('order/<int:product_id>/', views.place_order, name='place_order'),
]
