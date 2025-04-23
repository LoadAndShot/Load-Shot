from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Catalogue, Order
from .forms import CustomUserCreationForm, OrderForm
import os
import discord
from discord.ext import commands

# 🔒 Auth Views
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Identifiants invalides.')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# 🏠 Home / Présentation
@login_required
def dashboard_view(request):
    orders = Order.objects.filter(user=request.user)
    catalogues = Catalogue.objects.all()
    return render(request, 'dashboard.html', {'orders': orders, 'catalogues': catalogues})

# 🛒 Créer une commande
@login_required
def create_order_view(request, catalogue_id):
    catalogue = Catalogue.objects.get(id=catalogue_id)
    if (catalogue_id == 1 and request.user.lock_catalogue_1) or (catalogue_id == 2 and request.user.lock_catalogue_2):
        messages.error(request, 'Accès verrouillé à ce catalogue.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.catalogue = catalogue
            order.save()
            send_discord_order(order)
            messages.success(request, 'Commande passée avec succès !')
            return redirect('dashboard')
    else:
        form = OrderForm()
    return render(request, 'create_order.html', {'form': form, 'catalogue': catalogue})

# 📤 Discord Bot integration
def send_discord_order(order):
    import requests
    token = os.getenv('DISCORD_BOT_TOKEN')
    guild_id = os.getenv('DISCORD_GUILD_ID')
    legal_channel = os.getenv('DISCORD_LEGAL_CHANNEL_ID')
    illegal_channel = os.getenv('DISCORD_ILLEGAL_CHANNEL_ID')
    
    channel_id = legal_channel if order.catalogue.id == 1 else illegal_channel
    message = f"Nouvelle commande de {order.user.username} : {order.product.name} x{order.quantity} - Méthode : {order.delivery_method}"
    url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json"
    }
    payload = {"content": message}
    requests.post(url, headers=headers, json=payload)

