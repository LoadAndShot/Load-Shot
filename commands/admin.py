from django.contrib import admin
from .models import Product, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'catalogue', 'category')
    list_filter = ('catalogue', 'category')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'delivery_method', 'is_delivered', 'created_at')
    list_filter = ('is_delivered',)
