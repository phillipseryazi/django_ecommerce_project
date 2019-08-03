from django.db import models
from cloudinary.models import CloudinaryField
from ..users.models import User


# Create your models here.
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_product_fk')
    name = models.CharField(max_length=255)
    details = models.TextField()
    price = models.IntegerField(default=0)
    image = CloudinaryField('image')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)


class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_rating_fk')
    user = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
