from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (View, UpdateView, DeleteView, DetailView)
from django.views.generic.list import (ListView, )
from .forms import AddProductForm, UpdateProductForm
from .models import Product
from django.contrib import auth
import cloudinary
from django.core.paginator import Paginator
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


# Create your views here.
class HomeView(ListView):
    model = Product
    template_name = 'products/home.html'

    def get_queryset(self):
        queryset = Product.objects.all().order_by('id')
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'products' in cache:
            products_list = cache.get('products')
        else:
            products_list = self.get_queryset()
            cache.set('products', products_list, timeout=CACHE_TTL)

        paginator = Paginator(products_list, 6)
        page = self.request.GET.get('page')
        products = paginator.get_page(page)
        context['products'] = products
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
        if 'my_products' in cache:
            products_list = cache.get('my_products')
        else:
            products_list = self.get_queryset()
            cache.set('my_products', products_list, timeout=CACHE_TTL)

        paginator = Paginator(products_list, 6)
        page = self.request.GET.get('page')
        products = paginator.get_page(page)
        context['products'] = products
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
        paginator = Paginator(self.get_queryset(), 6)
        page = self.request.GET.get('page')
        products = paginator.get_page(page)
        context['products'] = products
        return context
