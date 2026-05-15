from django.urls import path
from .views import OffersListView, SingleOfferView, SingleDetailsOfferView

urlpatterns = [
    path('offers/', OffersListView.as_view(), name="offer-list"), #View for creating offers
    path('offers/<int:pk>/', SingleOfferView.as_view(), name="offer-detail"), #View for retrieving offer details
    path('offerdetails/<int:pk>/', SingleDetailsOfferView.as_view(), name="offer-details-detail"), #View for retrieving offer details
]

