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
            return OrderListSerializer
        
    def get_permissions(self):
        if self.request.method == 'PATCH':
            permission_classes = [IsAuthenticated, IsUserBusiness]
        elif self.request.method == 'DELETE':
            permission_classes = [IsAuthenticated, IsUserAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
class InProgressOrderListView(APIView):
    """
    API view to list all orders that are currently in progress.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Retrieves the count of orders that are currently in progress for a specific business user.
        """

        bussiness_user_id = self.kwargs.get('pk')

        try:
            business_profile = BusinessProfile.objects.get(user__id=bussiness_user_id)
        except BusinessProfile.DoesNotExist:
            return Response({"detail": "Business profile not found."}, status=status.HTTP_404_NOT_FOUND)
        
        order_count_in_progress = Order.objects.filter(business_user=business_profile, status='in_progress').count()
        return Response({"in_progress_order_count": order_count_in_progress}, status=status.HTTP_200_OK)
