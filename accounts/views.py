from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

# Page d'accueil après connexion
@login_required
def home(request):
    user = request.user
    is_admin = user.is_staff or user.is_superuser
    can_access_catalogue1 = user.can_access_catalogue1
    can_access_catalogue2 = user.can_access_catalogue2

    context = {
        'is_admin': is_admin,
        'can_access_catalogue1': can_access_catalogue1,
        'can_access_catalogue2': can_access_catalogue2,
    }
    return render(request, 'home.html', context)

# Inscription
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Compte créé avec succès. Connecte-toi maintenant.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

# Connexion
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, 'login.html')

# Déconnexion
def logout_view(request):
    logout(request)
    return redirect('login')

