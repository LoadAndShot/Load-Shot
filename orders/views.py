from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Order
from .forms import OrderForm

# 🏠 Page d'accueil (fixé proprement)
def home_view(request):
    return render(request, 'home.html')

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

# 🔒 Connexion
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

# 🚪 Déconnexion
def logout_view(request):
    logout(request)
    return redirect('login')

# 📦 Dashboard utilisateur + historique des commandes
@login_required
def dashboard_view(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'orders': orders})

# 📝 Créer une commande (sans catalogue pour l’instant)
@login_required
def create_order_view(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.description = request.POST.get('description')
            order.save()
            import discord
import os

from asgiref.sync import async_to_sync
from discord import Intents

def send_discord_order(order):
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    LEGAL_CHANNEL_ID = int(os.getenv('DISCORD_LEGAL_CHANNEL_ID'))
    ILLEGAL_CHANNEL_ID = int(os.getenv('DISCORD_ILLEGAL_CHANNEL_ID'))

    intents = Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        channel_id = LEGAL_CHANNEL_ID if not order.is_illegal else ILLEGAL_CHANNEL_ID
        channel = client.get_channel(channel_id)
        if channel:
            await channel.send(
                f"💥 Nouvelle commande de {order.user.username} : {order.description} "
                f"({order.quantity}x) - {'Illégal' if order.is_illegal else 'Légal'} - {order.delivery_method}"
            )
        await client.close()

    async_to_sync(client.start)(TOKEN)

            return redirect('dashboard')
    else:
        form = OrderForm()
    return render(request, 'create_order.html', {'form': form})
