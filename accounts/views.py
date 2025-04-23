from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from commands.models import Product, Order
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import CustomUserCreationForm

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def catalogue1(request):
    products = Product.objects.filter(catalogue=1)
    return render(request, 'catalogue1.html', {'products': products})

@login_required
def catalogue2(request):
    products = Product.objects.filter(catalogue=2)
    return render(request, 'catalogue2.html', {'products': products})

@login_required
def place_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        delivery_method = request.POST.get('delivery_method')
        order = Order.objects.create(
            client=request.user,
            product=product,
            quantity=int(request.POST.get('quantity')),
            delivery_method=delivery_method
        )
        messages.success(request, 'Commande passée avec succès !')
        return redirect('dashboard')
    return render(request, 'place_order.html', {'product': product})
