from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View

from runner.bootstraper import get_bootstrapper
from . import dataclasses
from .forms import ProductForm, TicketForm, FollowUpForm
from .models import Ticket


class ProductListView(View):
    template_name = 'tickets/product_list.html'
    ticket_service = get_bootstrapper().get_ticket_service()

    def get(self, request, organization_name=None):
        filters = dataclasses.ProductFilter(**request.GET)
        products = self.ticket_service.get_products(organization_name)
        context = {
            'products': products.results,
            'filters': filters,
        }

        return render(request, self.template_name, context)


class ProductView(View):
    template_name = 'tickets/product.html'
    service = get_bootstrapper().get_ticket_service()
    product_form = ProductForm
    ticket_form = TicketForm

    def get(self, request, product_uid):
        product = self.service.get_product(product_uid)
        tickets = self.service.get_tickets(product_uid=product_uid)
        context = {
            'product': product,
            'tickets': tickets,
            'ticket_form': self.ticket_form(),
        }

        return render(request, self.template_name, context)

    def post(self, request, product_uid):
        product = self.service.get_product(product_uid)
        form = self.ticket_form(request.POST)
        if form.is_valid():
            ticket_data = dataclasses.Ticket(**form.cleaned_data)
            ticket_data.product = product
            ticket_data.owner = request.user.username
            ticket = self.service.create_ticket(request.user.username, ticket_data)
            return redirect('ticket', ticket.uid)
        else:
            tickets = self.service.get_tickets(product_uid=product_uid)
            context = {
                'product': product,
                'tickets': tickets,
                'ticket_form': form,
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


class TicketDetailView(View):
    template_name = 'tickets/ticket.html'
    service = get_bootstrapper().get_ticket_service()
    account_service = get_bootstrapper().get_account_service()
    follow_up_form = FollowUpForm

    def get(self, request, ticket_uid):
        ticket = self.service.get_tickets(uid=ticket_uid)[0]
        follow_ups = self.service.get_follow_ups(ticket_uid=ticket_uid)
        if request.user.is_agent:
            users = self.account_service.get_agents(request.user)
        else:
            users = None
        form = self.follow_up_form()
        context = {
            'ticket': ticket,
            'follow_ups': follow_ups,
            'users': users,
            'follow_up_form': form,
            'STATUS_CHOICES': Ticket.STATUS_CHOICES
        }
        return render(request, self.template_name, context)

    def post(self, request, ticket_uid):
        ticket = self.service.get_tickets(uid=ticket_uid)[0]
        if 'title' in request.POST:
            follow_up_form = FollowUpForm(request.POST)
            if follow_up_form.is_valid():
                follow_up = dataclasses.FollowUp(**follow_up_form.cleaned_data)
                follow_up.ticket_uid = ticket_uid
                follow_up.user = request.user.username
                self.service.add_follow_up(
                    username=request.user.username,
                    follow_up_data=follow_up,
                    ticket_data=ticket,
                )
                return redirect('ticket', ticket_uid=ticket.uid)
        elif 'status' in request.POST:
            new_status = request.POST['status']
            self.service.change_status_ticket(
                username=request.user.username,
                ticket_data=ticket,
                status=new_status,
            )
            messages.success(request, f"ticket status changes successfully.")
            return redirect('ticket', ticket_uid=ticket.uid)
        elif 'assigned_user' in request.POST:
            assigned_user = request.POST['assigned_user']
            self.service.assign_ticket(
                username=request.user.username,
                ticket_data=ticket,
                to_be_assigned_username=assigned_user
            )
            return redirect('ticket', ticket_uid=ticket.uid)
        return redirect('ticket', ticket_uid=ticket_uid)
