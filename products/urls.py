from django.urls import path
from . import views

urlpatterns = [
    path('category/', views.category_list, name='category-list'),
    path('category/<int:pk>/', views.category_detail, name='category-detail'),
    path('products/', views.product_list, name='product-list'),
    path('products/<int:pk>/', views.product_detail, name='product-detail'),
    path('products/upload/', views.product_upload, name='product-upload'),
]