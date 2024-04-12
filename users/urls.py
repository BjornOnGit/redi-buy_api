from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('verify_seller/', views.seller_verification, name='seller-verification'),
    path('password_request/', views.password_request, name='password-request'),
    path('password_reset/', views.password_reset, name='password-reset'),
    path('google-signup/', views.google_auth_redirect, name='google_signup'),
    path('google-redirect/', views.google_redirect, name='google_redirect'),
    path('seller/', views.seller_profile, name='seller-profile'),
    path('buyer/', views.buyer_profile, name='buyer-profile'),
]