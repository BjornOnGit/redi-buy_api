from django.db import models
from users.models import SellerProfile

class Category(models.Model):
    name = models.CharField(max_length=100)

def __str__(self):
    return self.name

class Product(models.Model):
    seller = models.ForeignKey(SellerProfile, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    product_image = models.ImageField(upload_to='products/', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def __str__(self):
    return self.name
# Create your models here.
