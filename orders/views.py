from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Order
from django.contrib import messages

# 🟢 Page d'accueil
def home_view(request):
    return render(request, 'home.html')

# 🟢 Page de test CSS
def test_view(request):
    return render(request, 'test.html')

# 🟢 Inscription
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# 🟢 Connexion
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# 🟢 Déconnexion
def logout_view(request):
    logout(request)
    return redirect('home')

# 🟢 Dashboard utilisateur (commandes)
@login_required
def dashboard_view(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'orders': orders})

#
