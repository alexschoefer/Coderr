from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsBusinessUser
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import OfferCreateSerializer, OfferDetailsCreateSerializer, OfferDetailsSerializer, OfferListSerializer, SingleOfferDetailSerializer, SingleUpdateOfferSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.pagination import PageNumberPagination
from django.db.models import Min, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from offers_app.models import Offer



class PageSizeNumberPagination(PageNumberPagination):
    """
    Pagination class that allows clients to set the page size using a query parameter. Page size is 5 by default.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    

class OffersListView(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated]
    pagination_class = PageSizeNumberPagination

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ["updated_at", "annotated_min_price"]
    search_fields = ["title", "description"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OfferCreateSerializer
        return OfferListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = self._get_base_queryset()
        queryset = self._apply_filters(queryset)
        queryset = self._apply_search(queryset)
        return queryset


    def _get_base_queryset(self):
        """
        Base queryset with annotations and query optimizations.
        """
        return (
            Offer.objects
            .annotate(
                annotated_min_price=Min("offer_details__price"),
                annotated_min_delivery_time=Min("offer_details__delivery_time_in_days"),
            )
            .select_related("user", "user__user_details")
            .prefetch_related("offer_details")
        )


    def _apply_filters(self, queryset):
        """
        Apply query parameter filters.
        """
        creator_id = self.request.query_params.get("creator_id")
        if creator_id:
            queryset = queryset.filter(user_id=creator_id)

        min_price = self.request.query_params.get("min_price")
        if min_price:
            try:
                min_price = float(min_price)
            except (ValueError, TypeError):
                raise ValidationError({"min_price": "Must be a numeric value."})
            queryset = queryset.filter(annotated_min_price__gte=min_price)

        max_delivery_time = self.request.query_params.get("max_delivery_time")
        if max_delivery_time:
            try:
                max_delivery_time = int(max_delivery_time)
            except (ValueError, TypeError):
                raise ValidationError(
                    {"max_delivery_time": "Must be an integer value."}
                )
            queryset = queryset.filter(annotated_min_delivery_time__lte=max_delivery_time)

        return queryset


    def _apply_search(self, queryset):
        """
        Apply search filter on title and description.
        """
        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )
        return queryset

class SingleOfferView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Offer.objects.all()
    # serializer_class = SingleOfferDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        
        pk = self.kwargs.get("pk")
        return Offer.objects.filter(pk=pk).prefetch_related("offer_details")
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return SingleOfferDetailSerializer
        elif self.request.method == "PATCH":
            return SingleUpdateOfferSerializer
        elif self.request.method == "DELETE":
            pass
    
    def update(self, request, *args, **kwargs):
        # Handle PATCH request for updating offer details
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class SingleDetailsOfferView(generics.RetrieveAPIView):

    queryset = Offer.objects.all()
    serializer_class = OfferDetailsSerializer
    permission_classes = [IsAuthenticated]