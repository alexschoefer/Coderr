from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsBusinessUser
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import OfferCreateSerializer, OfferDetailsCreateSerializer, OfferDetailsSerializer, OfferListSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.pagination import PageNumberPagination
from django.db.models import Min
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from offers_app.models import Offer



class PageSizeNumberPagination(PageNumberPagination):
    """
    Pagination class that allows clients to set the page size using a query parameter. Page size is 5 by default.
    """
    page_size = 5
    page_size_query_param = 'page_size'
    

class OffersListView(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated]
    pagination_class = PageSizeNumberPagination

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ["updated_at", "min_price"]
    search_fields = ["title", "description"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OfferCreateSerializer
        return OfferListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):

        queryset = Offer.objects.annotate(
            min_price=Min("offer_details__price"),
            min_delivery_time=Min("offer_details__delivery_time_in_days"),
        ).select_related(
            "user",
            "user__user_details"
        ).prefetch_related(
            "offer_details"
        )

        creator_id = self.request.query_params.get("creator_id")
        min_price = self.request.query_params.get("min_price")
        max_delivery_time = self.request.query_params.get("max_delivery_time")

        if creator_id:
            queryset = queryset.filter(user_id=creator_id)

        if min_price:
            queryset = queryset.filter(min_price__gte=min_price)

        if max_delivery_time:
            queryset = queryset.filter(min_delivery_time__lte=max_delivery_time)

        return queryset

