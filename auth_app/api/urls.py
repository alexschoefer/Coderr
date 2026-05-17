# Django imports
from django.urls import path
from .views import RegistrationView, UserLoginView

urlpatterns = [
    path('registration/', RegistrationView.as_view(), name="registration"), #View for user registration
    path('login/', UserLoginView.as_view(), name="login") #View for user login
]