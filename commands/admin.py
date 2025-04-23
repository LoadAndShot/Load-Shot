from django.contrib import admin
from .models import Product, Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'is_delivered', 'created_at')  # plus de 'client' ni 'delivery_method'
    list_filter = ('is_delivered',)  # supprime 'delivery_method'
    search_fields = ('user__username', 'product__name')

