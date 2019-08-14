from django import forms
from .models import ShoppingCart


class CartForm(forms.ModelForm):
    class Meta:
        model = ShoppingCart
        fields = ['product', 'user', ]
