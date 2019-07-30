from django import forms
from .models import User


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control col-md-12', 'placeholder': 'username'}
    ), label=False)
    email = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control col-md-12 mt-4', 'placeholder': 'email', 'type': 'email'}
    ), label=False)
    phone = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control col-md-12 mt-4', 'placeholder': 'phone'}
    ), label=False)
    password = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control col-md-12 mt-4', 'placeholder': 'password', 'type': 'password'}
    ), label=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password',)

