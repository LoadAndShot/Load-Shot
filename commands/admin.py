from django.contrib import admin
from .models import Product, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'catalogue')
    list_filter = ('catalogue',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('client', 'product', 'quantity', 'delivery_method', 'created_at')
    list_filter = ('delivery_method', 'created_at')
