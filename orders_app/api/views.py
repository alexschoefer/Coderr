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
    serializer_class = OrderListSerializer
    # queryset = Order.objects.all()

    def get_queryset(self):
        """Returns a queryset of orders based on the type of the authenticated user."""
        user = self.request.user

        if user.type == "customer":
            return Order.objects.filter(customer_user__user=user)

        if user.type == "business":
            return Order.objects.filter(business_user__user=user)

        return Order.objects.none()
        
    def create(self, request, *args, **kwargs):
        """Handles the creation of a new order based on the provided offer details and the authenticated user."""
        serializer = OrderCreateSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        return Response(OrderListSerializer(order).data, status=201)
    
    def get_permissions(self):
        """Returns the appropriate permission classes based on the HTTP method of the request."""
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
            permission_classes = [IsUserBusiness]
        elif self.request.method == 'DELETE':
            permission_classes = [IsUserAdmin]
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
        return Response({"order_count": order_count_in_progress}, status=status.HTTP_200_OK)
    
class CompletedOrderCountListView(APIView):
    """
    API view to list all orders that are currently completed.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Retrieves the count of orders that are currently completed for a specific business user.
        """

        bussiness_user_id = self.kwargs.get('pk')

        try:
            business_profile = BusinessProfile.objects.get(user__id=bussiness_user_id)
        except BusinessProfile.DoesNotExist:
            return Response({"detail": "Business profile not found."}, status=status.HTTP_404_NOT_FOUND)
        
        order_count_completed = Order.objects.filter(business_user=business_profile, status='completed').count()
        return Response({"completed_order_count": order_count_completed}, status=status.HTTP_200_OK)
