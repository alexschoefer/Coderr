from django.urls import path
from .views import OffersListView, SingleOfferView, SingleDetailOfferView

urlpatterns = [
    path('api/offers/', OffersListView.as_view(), name="offer-create"), #View for creating offers
    path('api/offers/<int:pk>/', SingleDetailOfferView.as_view(), name="offer-detail"), #View for retrieving offer details
]

