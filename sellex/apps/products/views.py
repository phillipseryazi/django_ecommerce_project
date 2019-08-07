from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views.generic import (View, UpdateView, DeleteView, DetailView)
from django.views.generic.list import (ListView, )
from .forms import AddProductForm, UpdateProductForm, SearchForm
from .models import Product
from django.contrib import auth
import cloudinary


# Create your views here.
class HomeView(ListView):
    model = Product
    template_name = 'products/home.html'

    def get_queryset(self):
        queryset = Product.objects.all().order_by('id')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.get_queryset()
        return context


class PostProductView(View):
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


class MyProductsListView(ListView):
    model = Product
    template_name = 'products/my_products.html'

    def get_queryset(self):
        current_user = auth.get_user(self.request)
        queryset = Product.objects.filter(user_id=current_user).order_by('id')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.get_queryset()
        return context


class UpdateMyProduct(UpdateView):
    model = Product
    form_class = UpdateProductForm
    template_name = 'products/update_product.html'
    success_url = reverse_lazy('prods:my_products')


class DeleteProductView(DeleteView):
    model = Product
    success_url = reverse_lazy('prods:my_products')


class ProductDetailsView(DetailView):
    def get_queryset(self):
        queryset = Product.objects.filter(id=self.kwargs['pk'])
        return queryset


class SearchProductsView(ListView):
    model = Product
    template_name = 'products/home.html'

    def get_queryset(self):
        query = self.request.GET.get('search')
        queryset = Product.objects.filter(name__icontains=query).order_by('id')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.get_queryset()
        return context
