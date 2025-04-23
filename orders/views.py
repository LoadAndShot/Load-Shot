from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, OrderForm
from .models import Order

# Page d'accueil
def home(request):
    # Si l'utilisateur est authentifié, le rediriger éventuellement vers le tableau de bord
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'orders/home.html')

# Inscription d'un nouvel utilisateur
def signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # création du nouvel utilisateur
            # Authentification et connexion automatique de l'utilisateur après inscription
            raw_password = form.cleaned_data['password1']
            user = authenticate(username=user.username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'orders/signup.html', {'form': form})

# Connexion de l'utilisateur
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Identifiants valides, connexion de l'utilisateur
            user = form.get_user()
            login(request, user)
            # Redirection vers la page initialement demandée ou le tableau de bord
            next_url = request.POST.get('next')
            return redirect(next_url if next_url else 'dashboard')
    else:
        form = AuthenticationForm()
    # Si on arrive ici, soit c'est un GET, soit le formulaire n'était pas valide
    next_url = request.GET.get('next') or request.POST.get('next')
    # Changer les étiquettes du formulaire en français
    form.fields['username'].label = "Nom d'utilisateur"
    form.fields['password'].label = "Mot de passe"
    return render(request, 'orders/login.html', {'form': form, 'next': next_url})

# Déconnexion de l'utilisateur
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

# Tableau de bord de l'utilisateur (liste des commandes)
@login_required
def dashboard(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/dashboard.html', {'orders': orders})

# Création d'une nouvelle commande
@login_required
def new_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user  # associer la commande à l'utilisateur connecté
            order.save()
            # La commande est créée avec sent_to_discord=False par défaut.
            # Le bot Discord prendra en charge l'envoi de la commande au channel approprié.
            return redirect('dashboard')
    else:
        form = OrderForm()
    return render(request, 'orders/new_order.html', {'form': form})

