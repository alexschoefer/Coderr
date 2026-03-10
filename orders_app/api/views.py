from rest_framework import generics
from .serializers import OrderListSerializer, OrderCreateSerializer
from offers_app.models import OfferDetails
from orders_app.models import Order
from rest_framework.permissions import IsAuthenticated
from .permissions import IsUserCustomer, IsUserAdmin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from profil_app.models import CustomerProfile, BusinessProfile

class OrderListAPIView(generics.ListCreateAPIView):
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

        