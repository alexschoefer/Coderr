from rest_framework import generics
from .serializers import OrderListSerializer
from offers_app.models import OfferDetails
from orders_app.models import Order
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from profil_app.models import CustomerProfile, BusinessProfile

class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]

    def _check_offer_details(self, offer_details_id):
        if not offer_details_id:
            return Response({"error": "offer_details_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            return OfferDetails.objects.get(id=offer_details_id), None
        except OfferDetails.DoesNotExist:
            return None, Response({"error": "OfferDetails with the provided ID does not exist."}, status=status.HTTP_404_NOT_FOUND)
        except (ValueError, TypeError):
            return None, Response({"error": "Invalid offer_details_id format. It musst be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)