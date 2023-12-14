from django.shortcuts import render
from django.contrib.auth.views import LoginView


def index(request):
    return render(request, 'base.html')


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'  # Replace with your actual template name
    success_url = 'home'  # Replace with the URL name or path where the user should be redirected after login