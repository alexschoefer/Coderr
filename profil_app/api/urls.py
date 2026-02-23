# Django imports
from django.urls import path

# Local imports
from profil_app.api.views import UserProfileView, BusinessProfileListView, CustomerProfileListView

urlpatterns = [
    path('api/profile/<int:pk>/', UserProfileView.as_view(), name='customer-profile'),
    path('api/profiles/business/', BusinessProfileListView.as_view(), name='business-profile-list'),
    path('api/profiles/customer/', CustomerProfileListView.as_view(), name='customer-profile-list'),
]