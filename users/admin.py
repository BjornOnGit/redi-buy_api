from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, SellerProfile, BuyerProfile

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email',
                    'is_staff',
                    'is_active',
                    ]
    fieldsets = UserAdmin.fieldsets
    add_fieldsets = UserAdmin.add_fieldsets

class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'business_name', 'bio',
                    'phone_number', 'address',
                    'profile_picture', 'rating', 'receive_notifications']

class BuyerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'address',
                    'profile_picture', 'receive_notifications']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(SellerProfile, SellerProfileAdmin)
admin.site.register(BuyerProfile, BuyerProfileAdmin)

# Register your models here.
