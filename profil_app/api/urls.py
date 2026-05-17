# Django imports
from django.urls import path

# Local imports
from profil_app.api.views import UserProfileView, BusinessProfileListView, CustomerProfileListView

urlpatterns = [
    path('profile/<int:pk>/', UserProfileView.as_view(), name='customer-profile'),
    path('profiles/business/', BusinessProfileListView.as_view(), name='business-profile-list'),
    path('profiles/customer/', CustomerProfileListView.as_view(), name='customer-profile-list'),
]