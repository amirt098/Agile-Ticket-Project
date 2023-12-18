

from django.urls import path
from . import views

urlpatterns = [
    path('product/create/', views.CreateProductView.as_view(), name='create_product'),
    path('product/', views.ProductListView.as_view(), name='get_products'),
]