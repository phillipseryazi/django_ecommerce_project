from django.shortcuts import render, redirect
from django.views.generic import (View, )
from .forms import AddProductForm, UpdateProductForm
from django.contrib import auth
import cloudinary


# Create your views here.
class HomeView(View):
    def get(self, request):
        return render(request, 'products/home.html', {'form': ''})


class ProductView(View):
    def get(self, request):
        form = AddProductForm()
        return render(request, 'products/add_product.html', {'form': form})

    def post(self, request):
        form = AddProductForm(request.POST, request.FILES)
        image_url = cloudinary.uploader.upload(request.FILES['image'])['url']
        if form.is_valid():
            current_user = auth.get_user(request)
            form.instance.user = current_user
            form.instance.image = image_url
            form.save()
            return redirect('prods:manage_product')

        form = AddProductForm()
        return render(request, 'products/add_product.html', {'form': form})

    # def put(self, request):
    #     form = AddProductForm(request.PUT)
    #     pass
    #
    # def delete(self, request):
    #     pass
