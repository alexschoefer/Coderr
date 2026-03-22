from rest_framework import generics
from .serializers import ReviewListSerializer, SingleReviewSerializer
from reviews_app.models import Review
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOfReview, IsUserAuthorizedToCreateReview
from rest_framework.exceptions import ValidationError
from profil_app.models import CustomerProfile, BusinessProfile
from rest_framework.filters import OrderingFilter
from rest_framework.exceptions import PermissionDenied

class ReviewListCreateAPIView(generics.ListCreateAPIView):
    """
    API view for listing and creating reviews. Users can filter reviews by business_user_id and reviewer_id, and order them by updated_at and rating. 
    Only authenticated users can access this view, and only authorized users can create reviews.
    """

    ordering_fields = ["updated_at", "rating"]
    ordering = ["-updated_at"]

    def get_permissions(self):
        """Set permissions based on the request method."""
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsUserAuthorizedToCreateReview()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        """Return the appropriate serializer class based on the request method."""
        if self.request.method == 'POST':
            return SingleReviewSerializer
        return ReviewListSerializer
    
    def get_queryset(self):
        queryset = Review.objects.all()

        business_user_id = self.request.query_params.get("business_user_id")
        if business_user_id:
            queryset = queryset.filter(business_user__user__id=business_user_id)

        reviewer_id = self.request.query_params.get("reviewer_id")
        if reviewer_id:
            queryset = queryset.filter(reviewer__user__id=reviewer_id)

        return queryset
    
    def _get_customer_profile(self, user):
        """Helper method to retrieve the customer profile for the current user."""
        try:
            return CustomerProfile.objects.get(user=self.request.user)
        except CustomerProfile.DoesNotExist:
            raise ValidationError("Customer profile does not exist for the current user.")
        

    def _get_business_profile(self, business_user_id):
        """Helper method to retrieve the business profile based on the provided business user ID."""
        if not business_user_id:
            raise ValidationError("Business user ID is required.")

        try:
            return BusinessProfile.objects.get(user__id=business_user_id)
        except BusinessProfile.DoesNotExist:
            raise ValidationError("Business profile does not exist.")
    
    def perform_create(self, serializer):
        """Override the perform_create method to set the reviewer and business_user fields when creating a new review."""
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
    """
    API view for retrieving, updating, and deleting a single review. Only the owner of the review can update or delete it.
    """
    permission_classes = [IsOwnerOfReview, IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = SingleReviewSerializer