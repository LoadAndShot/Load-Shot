from django.contrib import admin
from .models import Product, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'catalogue')
    list_filter = ('catalogue',)
    search_fields = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'delivery_method', 'status', 'created_at')
    list_filter = ('delivery_method', 'status')
    search_fields = ('user__username', 'product__name')

