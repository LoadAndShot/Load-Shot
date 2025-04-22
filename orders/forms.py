from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['is_illegal', 'delivery_method', 'quantity']
        widgets = {
            'is_illegal': forms.CheckboxInput(),
            'delivery_method': forms.Select(),
            'quantity': forms.NumberInput(attrs={'min': 1}),
        }
