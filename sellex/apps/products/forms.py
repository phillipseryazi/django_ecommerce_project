from django import forms
from .models import Product


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'details', 'price', 'image')

    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control col-md-12 mt-2', 'placeholder': 'name'}
    ), label=False)
    details = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control col-md-12 mt-4', 'placeholder': 'details', 'rows': '3'}
    ), label=False)
    price = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control col-md-12 mt-4 mb-4', 'placeholder': 'price'}
    ), label=False)

    image = forms.CharField(widget=forms.FileInput(attrs={'class': 'form-control-file mb-4', 'name': 'image'}))


class UpdateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'details', 'price')

    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control col-md-12 mt-2', 'placeholder': 'name'}
    ), label=False)
    details = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control col-md-12 mt-4', 'placeholder': 'details', 'rows': '3'}
    ), label=False)
    price = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control col-md-12 mt-4 mb-4', 'placeholder': 'price'}
    ), label=False)


class SearchForm(forms.Form):
    product = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control col-md-6 mt-2', 'placeholder': 'product'}
    ), label=False)
