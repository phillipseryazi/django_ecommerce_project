from django.db import models


# Create your models here.
class ShoppingCart(models.Model):
    product = models.IntegerField(default=0)
    user = models.IntegerField(default=0)


class Order(models.Model):
    product = models.IntegerField(default=0)
    user = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
