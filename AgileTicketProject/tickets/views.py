from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View

from runner.bootstraper import get_bootstrapper
from . import dataclasses
from .forms import ProductForm


class ProductListView(View):
    template_name = 'tickets/product_list.html'
    ticket_service = get_bootstrapper().get_ticket_service()

    def get(self, request):
        filters = dataclasses.ProductFilter(**request.GET)
        products = self.ticket_service.get_products(filters=filters)
        context = {
            'products': products.results,
            'filters': filters,
        }

        return render(request, self.template_name, context)


class CreateProductView(View):
    template_name = 'tickets/create_product.html'
    service = get_bootstrapper().get_ticket_service()
    product_form = ProductForm

    def get(self, request):
        form = self.product_form()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.product_form(request.POST)
        if form.is_valid():
            try:
                product_data = dataclasses.Product(**form.cleaned_data)
                result = self.service.create_product(product_data=product_data, agent_data=request.user)
                messages.success(request, f'Product {result.name} created success fully.')
                return redirect('create_product')
            except Exception as e:
                messages.error(request, f"Error during product creation: {e}")
                raise e
        else:
            return render(request, self.template_name, {'form': form})


class DashboardView(View):
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
