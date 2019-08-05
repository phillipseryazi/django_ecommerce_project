from django.urls import path
from .views import (HomeView, PostProductView, MyProductsListView, UpdateMyProduct, DeleteProductView)

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('manage/', PostProductView.as_view(), name='manage_product'),
    path('myproducts/', MyProductsListView.as_view(), name='my_products'),
    path('update/<int:pk>/', UpdateMyProduct.as_view(), name='update_product'),
    path('delete/<int:pk>/', DeleteProductView.as_view(), name='delete_product'),
]
