from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Order

# Formulaire d'inscription (création de compte utilisateur)
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)
        labels = {
            'username': "Nom d'utilisateur"
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Changer les libellés par défaut des champs de mot de passe en français
        self.fields['password1'].label = "Mot de passe"
        self.fields['password2'].label = "Confirmation du mot de passe"

# Formulaire de création d'une nouvelle commande
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product_type', 'method']
        labels = {
            'product_type': 'Type de produit',
            'method': 'Méthode'
        }
