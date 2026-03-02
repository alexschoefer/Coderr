from django.urls import path
from .views import OffersListView

urlpatterns = [
    path('api/offers/', OffersListView.as_view(), name="offer-create"), #View for creating offers
]

