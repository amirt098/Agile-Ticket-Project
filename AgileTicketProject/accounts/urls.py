from django.urls import path
from .views import UserLoginView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    # Other URL patterns for the app
]