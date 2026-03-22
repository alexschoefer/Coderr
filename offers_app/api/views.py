from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsBusinessUser, SingleOfferPermission, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import OfferCreateSerializer, OfferDetailsCreateSerializer, OfferDetailsSerializer, OfferListSerializer, SingleOfferSerializer, SingleUpdateOfferSerializer, SingleDeleteOfferSerializer, SingleDetailOfferSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.pagination import PageNumberPagination
from django.db.models import Min, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from offers_app.models import Offer, OfferDetails



class PageSizeNumberPagination(PageNumberPagination):
    """
    Pagination class that allows clients to set the page size using a query parameter. Page size is 5 by default.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    

class OffersListView(generics.ListCreateAPIView):
    """
    View for listing all offers and creating new offers. Supports filtering by creator, minimum price, and maximum delivery time, as well as searching by title and description.
    """

    pagination_class = PageSizeNumberPagination

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ["updated_at", "annotated_min_price"]
    search_fields = ["title", "description"]

    def get_permissions(self):
        """Return different permissions based on the request method. Only business users can create offers, while all authenticated users can view offers."""
        if self.request.method == "POST":
            return [IsBusinessUser()]
        return [IsAuthenticatedOrReadOnly()]

    def get_serializer_class(self):
        """Return different serializers based on the request method. Use OfferCreateSerializer for POST requests and OfferListSerializer for GET requests."""
        if self.request.method == "POST":
            return OfferCreateSerializer
        return OfferListSerializer

    def perform_create(self, serializer):
        """Override the default create behavior to associate the new offer with the authenticated user."""
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """"Override the default queryset to apply custom filtering and searching logic."""
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
    """
    View for retrieving, updating, and deleting a single offer. 
    Only the owner of the offer can update or delete it, while all authenticated users can view the offer details.
    """
    queryset = Offer.objects.all()
    permission_classes = [SingleOfferPermission]

    def get_queryset(self):
        """Override the default queryset to prefetch related offer details for the specific offer being accessed."""
        pk = self.kwargs.get("pk")
        return Offer.objects.filter(pk=pk).prefetch_related("offer_details")
    
    def get_serializer_class(self):
        """
        Return different serializers based on the request method. 
        Use SingleOfferSerializer for GET requests, SingleUpdateOfferSerializer for PATCH requests, and SingleDeleteOfferSerializer for DELETE requests.
        """
        if self.request.method == "GET":
            return SingleOfferSerializer
        elif self.request.method == "PATCH":
            return SingleUpdateOfferSerializer
        elif self.request.method == "DELETE":
            return SingleDeleteOfferSerializer
    
    def update(self, request, *args, **kwargs):
        """Override the default update behavior to allow partial updates (PATCH) and ensure that only the owner of the offer can update it."""
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class SingleDetailsOfferView(generics.RetrieveAPIView):
    """View for retrieving the details of a single offer detail. All authenticated users can view the offer detail information."""
    queryset = OfferDetails.objects.all()
    serializer_class = SingleDetailOfferSerializer
    permission_classes = [IsAuthenticated]
