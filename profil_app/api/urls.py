# Django imports
from django.urls import path

# Local imports
from profil_app.api.views import UserProfileView

urlpatterns = [
    path('api/profile/<int:pk>/', UserProfileView.as_view(), name='customer-profile'),
]