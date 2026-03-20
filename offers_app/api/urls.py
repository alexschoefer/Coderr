from django.urls import path
from .views import OffersListView, SingleOfferView, SingleDetailsOfferView

urlpatterns = [
    path('api/offers/', OffersListView.as_view(), name="offer-list"), #View for creating offers
    path('api/offers/<int:pk>/', SingleOfferView.as_view(), name="offer-detail"), #View for retrieving offer details
    path('api/offerdetails/<int:pk>/', SingleDetailsOfferView.as_view(), name="offer-details-detail"), #View for retrieving offer details
]

