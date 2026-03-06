from django.urls import path
from .views import OffersListView, SingleOfferView

urlpatterns = [
    path('api/offers/', OffersListView.as_view(), name="offer-create"), #View for creating offers
    path('api/offers/<int:pk>/', SingleOfferView.as_view(), name="offer-detail"), #View for retrieving offer details
]

