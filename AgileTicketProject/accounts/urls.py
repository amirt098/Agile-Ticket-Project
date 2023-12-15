from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('create_user/', views.CreateUserView.as_view(), name='create_user'),
    path('create_agent/', views.CreateAgentView.as_view(), name='create_agent'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('create_organization/', views.CreateOrganizationView.as_view(), name='create_organization'),

    # Other URL patterns for the app
]