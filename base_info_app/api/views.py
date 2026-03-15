from rest_framework import generics
from base_info_app.models import BaseInfo
from base_info_app.api.serializers import BaseInfoSerializer
from rest_framework.permissions import AllowAny
from reviews_app.models import Review
from profil_app.models import BusinessProfile
from offers_app.models import Offer
from rest_framework.response import Response
from django.db.models import Avg

class BaseInfoAPIView(generics.RetrieveAPIView):
    """
    API view to retrieve aggregated base information about reviews, business profiles, and offers.
    This view provides read-only access to the aggregated data stored in the BaseInfo model.
    """

    queryset = BaseInfo.objects.all()
    serializer_class = BaseInfoSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Override the get method to return aggregated data from the BaseInfo model.
        """

        review_count = Review.objects.count()
        average_rating = Review.objects.aggregate(Avg('rating'))['rating__avg'] or 0
        business_profile_count = BusinessProfile.objects.count()
        offer_count = Offer.objects.count()
        data = {
            'review_count': review_count,
            'average_rating': average_rating,
            'business_profile_count': business_profile_count,
            'offer_count': offer_count
        }

        return Response(data)
