from django.urls import path
from .views import HomeView, ProductView

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('manage/', ProductView.as_view(), name='manage_product')
]
