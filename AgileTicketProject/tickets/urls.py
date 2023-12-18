

from django.urls import path
from . import views

urlpatterns = [
    path('product/create/', views.ProductCreateView.as_view(), name='product_create'),
]