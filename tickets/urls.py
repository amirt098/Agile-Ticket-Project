

from django.urls import path
from . import views

urlpatterns = [
    path('product/create/', views.CreateProductView.as_view(), name='create_product'),
    path('product/<str:product_uid>', views.ProductView.as_view(), name='product'),
    path('modify_product/<str:product_uid>', views.ModifyProductView.as_view(), name='modify_product'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<str:organization_name>/', views.ProductListView.as_view(), name='org_product_list'),
    path('ticket/<str:ticket_uid>/', views.TicketDetailView.as_view(), name='ticket'),
    path('modify_ticket/<str:ticket_uid>', views.ModifyTicketView.as_view(), name='modify_ticket'),
    path('assigned/', views.AssignedTicketListView.as_view(), name='assigned_ticket'),
    path('un_assigned/', views.UnAssignedTicketListView.as_view(), name='un_assigned_ticket'),

]