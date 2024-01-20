from django.contrib import admin

from . models import Product, FollowUp, Ticket

admin.site.register(Product)
admin.site.register(FollowUp)
admin.site.register(Ticket)
