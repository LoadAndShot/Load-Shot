from django.contrib import admin
from .models import Product, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'catalog', 'price')  # catalog (pas catalogue)
    list_filter = ('catalog',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'product', 'delivery_method', 'created_at')  # 'client' pas 'user'
    list_filter = ('delivery_method', 'created_at')
