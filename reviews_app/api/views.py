from rest_framework import generics
from .serializers import ReviewListSerializer, SingleReviewSerializer
from reviews_app.models import Review
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOfReview, IsUserAuthorizedToCreateReview
from rest_framework.exceptions import ValidationError
from profil_app.models import CustomerProfile, BusinessProfile
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.exceptions import PermissionDenied

class ReviewListCreateAPIView(generics.ListCreateAPIView):

    filter_backends = [DjangoFilterBackend, OrderingFilter]

    filterset_fields = ["business_user_id", "reviewer_id"]

    ordering_fields = ["updated_at", "rating"]
    ordering = ["-updated_at"]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsUserAuthorizedToCreateReview()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SingleReviewSerializer
        return ReviewListSerializer
    
    def get_queryset(self):
        queryset = Review.objects.all()

        business_user_id = self.request.query_params.get("business_user_id")
        if business_user_id:
            queryset = queryset.filter(business_user__id=business_user_id)

        reviewer_id = self.request.query_params.get("reviewer_id") 
        if reviewer_id:
            queryset = queryset.filter(reviewer__id=reviewer_id)

        return queryset
    
    def _get_customer_profile(self, user):
        try:
            return CustomerProfile.objects.get(user=self.request.user)
        except CustomerProfile.DoesNotExist:
            raise ValidationError("Customer profile does not exist for the current user.")
        

    def _get_business_profile(self, business_user_id):

        business_user_id = self.request.data.get('business_user')
        if not business_user_id:
            raise ValidationError("Business user ID is required.")
        try:
            return BusinessProfile.objects.get(user=business_user_id)
        except BusinessProfile.DoesNotExist:
            raise ValidationError("Business profile does not exist for the provided business user ID.")
    
    def perform_create(self, serializer):

        customer_user = self._get_customer_profile(self.request.user)
        business_user = self._get_business_profile(self.request.data.get('business_user'))

        if Review.objects.filter(
            reviewer=customer_user,
            business_user=business_user
        ).exists():
            raise ValidationError("You have already reviewed this business.")

        serializer.save(
            reviewer=customer_user,
            business_user=business_user
        )

class ReviewRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsOwnerOfReview, IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = SingleReviewSerializer