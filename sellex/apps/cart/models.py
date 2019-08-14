from django.db import models


# Create your models here.
class ShoppingCart(models.Model):
    product = models.IntegerField(default=0)
    user = models.IntegerField(default=0)
