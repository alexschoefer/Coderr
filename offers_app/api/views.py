from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsBusinessUser
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import OfferCreateSerializer, OfferDetailsCreateSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

class OfferCreateView(generics.CreateAPIView):

    permission_classes = [IsAuthenticated, IsBusinessUser]
    serializer_class = OfferCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        offer = serializer.save(user=request.user)

        response_data = {
            "id": offer.id,
            "title": offer.title,
            "description": offer.description,
            "min_price": offer.min_price,
            "min_delivery_time": offer.min_delivery_time,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)