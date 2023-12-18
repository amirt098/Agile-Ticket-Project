from django.urls import path
from . import views

urlpatterns = [
    # path('login/user/', views.UserLoginView.as_view(), name='user_login'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/user/', views.CreateUserView.as_view(), name='register_user'),
    path('register/agent/', views.CreateAgentView.as_view(), name='register_agent'),
    path('modify/agent/<int:agent_id>', views.ModifyAgentView.as_view(), name='modify_agent'),
    path('modify/user/<int:user_id>', views.ModifyUserView.as_view(), name='modify_user'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('agent_management/', views.AgentManagementView.as_view(), name='agent_management'),
    path('register_organization/', views.CreateOrganizationView.as_view(), name='register_organization'),


    # Other URL patterns for the app
]