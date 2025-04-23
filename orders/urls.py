from django.urls import path
from . import views

# Routes URL de l'application 'orders'
urlpatterns = [
    path('', views.home, name='home'),                # Page d'accueil
    path('signup/', views.signup, name='signup'),     # Inscription
    path('login/', views.login_view, name='login'),   # Connexion
    path('logout/', views.logout_view, name='logout'),# Déconnexion
    path('dashboard/', views.dashboard, name='dashboard'),    # Tableau de bord utilisateur
    path('orders/new/', views.new_order, name='new_order'),   # Création d'une nouvelle commande
]
