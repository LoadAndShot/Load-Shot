from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('catalogue1/', views.catalogue1, name='catalogue1'),
    path('catalogue2/', views.catalogue2, name='catalogue2'),
    path('order/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/remove/<int:index>/', views.remove_from_cart, name='remove_from_cart'),  # <-- ici ajout du remove
    path('confirm_order/', views.confirm_order, name='confirm_order'),
]
