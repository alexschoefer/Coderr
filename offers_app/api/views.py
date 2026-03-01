from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsBusinessUser
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import OfferCreateSerializer, OfferDetailsCreateSerializer, OfferDetailsSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

class OfferCreateView(generics.CreateAPIView):

    permission_classes = [IsAuthenticated, IsBusinessUser]
    serializer_class = OfferCreateSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OfferCreateSerializer
        return OfferDetailsSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)

    #     offer = serializer.save(user=request.user)

    #     # Serialize offer details for the response
    #     details_serializer = OfferDetailsCreateSerializer(
    #         offer.offer_details_set.all(), many=True  # Corrected the attribute name
    #     )

    #     response_data = {
    #         "id": offer.id,
    #         "title": offer.title,
    #         "description": offer.description,
    #         "details": details_serializer.data,  # Include serialized details
    #     }

    #     return Response(response_data, status=status.HTTP_201_CREATED)

class OfferListView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.user_offers.all()