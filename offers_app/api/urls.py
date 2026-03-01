from django.urls import path
from .views import OfferCreateView

urlpatterns = [
    path('api/offers/', OfferCreateView.as_view(), name="offer-create"), #View for creating offers
]

