from django.shortcuts import render, redirect
from django.views import View

from runner.bootstraper import get_bootstrapper
from . import dataclasses
from .forms import ProductForm


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


class ProductCreateView(View):
    template_name = 'product_create.html'
    service = get_bootstrapper().get_ticket_service()

    def get(self, request):
        form = ProductForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            agent_data = request.user
            product_data = form.cleaned_data
            try:
                created_product = self.service.create_product(agent_data, product_data)
                return redirect('product_list')
            except Exception as e:
                form.add_error(None, str(e))
        return render(request, self.template_name, {'form': form})


class DashboardView(View):
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
