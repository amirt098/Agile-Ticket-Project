

from django.urls import path
from . import views

urlpatterns = [
    path('product/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('product/', views.ProductListView.as_view(), name='get_products'),
]