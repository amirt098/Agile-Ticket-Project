from django import forms

from .models import Product, Ticket, FollowUp


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'pre_set_reply', 'description', 'image']


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority', 'dead_line_date']
        widgets = {
            'dead_line_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class ModifyTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority']


class FollowUpForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        fields = ['title', 'text']
