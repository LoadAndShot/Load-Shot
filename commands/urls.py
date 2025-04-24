from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('catalogue1/', views.catalogue1, name='catalogue1'),
    path('catalogue2/', views.catalogue2, name='catalogue2'),
    path('order/<int:product_id>/', views.place_order, name='place_order'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/summary/', views.cart_summary, name='cart_summary'),
    path('cart/validate/', views.validate_cart, name='validate_cart'),
]
