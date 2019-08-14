from django.shortcuts import render, reverse, redirect
from django.urls import reverse_lazy
from django.views.generic import (View, DeleteView, ListView)
from .models import ShoppingCart
from ..products.models import Product
from django.contrib import auth
from django.core.paginator import Paginator


# Create your views here.
class AddToCartView(View):
    def get(self, request, **kwargs):
        cart = ShoppingCart()
        cart.product = kwargs['id']
        cart.user = kwargs['uid']
        cart.save()
        return redirect('prods:detail_product', pk=kwargs['id'])


class GetCartView(ListView):
    model = Product
    template_name = 'cart/cart.html'

    def get_queryset(self):
        current_user = auth.get_user(self.request)
        cart_items_list = ShoppingCart.objects.filter(user=current_user.id)
        product_list = []
        for item in cart_items_list:
            product = Product.objects.get(id=item.product)
            setattr(product, 'cart_id', item.id)
            product_list.append(product)
        return product_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 6)
        page = self.request.GET.get('page')
        products = paginator.get_page(page)
        context['products'] = products
        total = 0
        for item in queryset:
            total = total + item.price
        context['total'] = total
        return context


class RemoveFromCartView(DeleteView):
    model = ShoppingCart
    success_url = reverse_lazy('cart:get_cart')
