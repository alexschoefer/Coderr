from rest_framework import generics
from .serializers import OrderListSerializer, OrderCreateSerializer
from offers_app.models import OfferDetails
from orders_app.models import Order
from rest_framework.permissions import IsAuthenticated
from .permissions import IsUserCustomer, IsUserAdmin, IsUserBusiness
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from profil_app.models import CustomerProfile, BusinessProfile

class OrderListAPIView(generics.ListCreateAPIView):
    """
    API view to list all orders or create a new order.
    """
    queryset = Order.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderListSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [IsAuthenticated, IsUserCustomer]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

class SingleOrderView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a single order based on its ID.
    """
    queryset = Order.objects.all()

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the HTTP method of the request.
         - For PATCH requests, it returns OrderListSerializer to update an existing order.
         - For DELETE requests, it returns 10 (which seems to be a placeholder and should be replaced with an appropriate serializer or response).
         - For other methods (like GET), it defaults to OrderListSerializer.
        """

        if self.request.method == 'PATCH':
            return OrderListSerializer
        if self.request.method == 'DELETE':
            return 10
        
    def get_permissions(self):
        if self.request.method == 'PATCH':
            permission_classes = [IsAuthenticated, IsUserBusiness]
        elif self.request.method == 'DELETE':
            permission_classes = [IsAuthenticated, IsUserAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]