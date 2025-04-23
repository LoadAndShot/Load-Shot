from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'catalogue')
    list_filter = ('catalogue',)
    search_fields = ('name',)

