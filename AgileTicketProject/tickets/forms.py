from django import forms
from .models import Product

class CreateProductForm(forms.Form):
    name = forms.CharField(max_length=255)
    owner = forms.CharField(required=False)
    description = forms.CharField(required=False)

