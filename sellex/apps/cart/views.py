from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from django.urls import reverse_lazy
from django.views.generic import (View, DeleteView, ListView)
from .models import ShoppingCart
from ..products.models import Product
from django.contrib import auth
from django.core.paginator import Paginator
from django.conf import settings
from .models import Order
import stripe


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


def get_total(queryset):
    total = 0
    for item in queryset:
        total = total + item.price
    return total


class PaymentView(View):
    current_user = 0

    def get_queryset(self):
        self.current_user = auth.get_user(self.request)
        cart_items_list = ShoppingCart.objects.filter(user=self.current_user.id)
        product_list = []
        for item in cart_items_list:
            product = Product.objects.get(id=item.product)
            setattr(product, 'cart_id', item.id)
            product_list.append(product)
        return product_list

    def get(self, request):
        context = dict()
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 6)
        page = self.request.GET.get('page')
        products = paginator.get_page(page)
        context['products'] = products
        total = get_total(queryset)
        context['total'] = total
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return render(request, 'cart/checkout.html', context)

    def post(self, request):
        queryset = self.get_queryset()
        total = get_total(queryset)

        for item in queryset:
            order = Order(user=self.current_user.id, product=item.id)
            order.save()

        stripe.api_key = settings.STRIPE_SECRET_KEY
        charge = stripe.Charge.create(
            amount=total,
            currency='usd',
            description='Sellex Charge',
            source=request.POST['stripeToken']
        )

        return HttpResponseRedirect(reverse('cart:get_cart'))
