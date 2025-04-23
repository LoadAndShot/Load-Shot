from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Order

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2')

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'quantity', 'delivery_method']

