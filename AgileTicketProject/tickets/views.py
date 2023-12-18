from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
import logging
from . import dataclasses
from .forms import CreateProductForm
from runner.bootstraper import get_bootstrapper
from . import dataclasses


class ProductListView(View):
    template_name = 'products/product_list.html'
    ticket_service = get_bootstrapper().get_ticket_service()

    def get(self, request, *args, **kwargs):
        filters = dataclasses.ProductFilter(**request.query_params)
        products = self.ticket_service.get_products(filters=filters)
        context = {
            'products': products.results,
            'filters': filters,
        }

        return render(request, self.template_name, context)



class CreateProductView(View):
    template_name = 'tickets/create_product.html'
    service = get_bootstrapper().get_ticket_service()
    product_form = CreateProductForm

    def get(self, request):
        form = self.product_form()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.product_form(request.POST)
        if form.is_valid():
            try:
                product_data = dataclasses.Product(**form.cleaned_data)
                if request.user.is_agent:
                    result = self.service.create_product(product_data= product_data,agent_data= request.user)
                    messages.success(request, f'Product {result.name} created success fully.')
                return redirect('create_product')
            except Exception as e:
                messages.error(request, f"Error during product creation: {e}")
                return redirect('create_product')
        else:
            return render(request, self.template_name, {'form': form})


class DashboardView(View):
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
