from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager
from django.utils import timezone

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    is_seller = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

def __str__(self):
    return self.email

class SellerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=100)
    bio = models.TextField()
    phone_number = models.CharField(max_length=11)
    address = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='seller_profile_pictures', null=True, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=2, default=0.0)
    receive_notifications = models.BooleanField(default=True)

class BuyerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11)
    address = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='buyer_profile_pictures', null=True, blank=True)
    wishlist = models.ManyToManyField('products.Product', related_name='wishlist', blank=True)
    receive_notifications = models.BooleanField(default=True)


class PasswordReset(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    expiration = models.DateTimeField()

    def __str__(self):
        return self.user.username
    
    def is_expired(self):
        return self.expiration < timezone.now()
# Create your models here.
