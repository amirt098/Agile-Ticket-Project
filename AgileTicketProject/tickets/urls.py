

from django.urls import path
from . import views

urlpatterns = [
    path('product/create/', views.CreateProductView.as_view(), name='create_product'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
]