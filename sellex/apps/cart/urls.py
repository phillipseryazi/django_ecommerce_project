from django.urls import path
from .views import AddToCartView, GetCartView, RemoveFromCartView

urlpatterns = [
    path('add/<int:id>/<int:uid>/', AddToCartView.as_view(), name='add_to_cart'),
    path('get/', GetCartView.as_view(), name='get_cart'),
    path('remove/<int:pk>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
]
