from django.db import models
from profil_app.models import BusinessProfile, CustomerProfile
from auth_app.models import CustomUser

class Review(models.Model):
    """
    Represents a review of a business by a customer.
     Attributes:
        business_user (BusinessProfile): The business profile being reviewed.
        reviewer (CustomerProfile): The customer profile writing the review.
        rating (int): The rating given by the reviewer.
        description (str): The description of the review.
        created_at (datetime): The date and time when the review was created.
        updated_at (datetime): The date and time when the review was last updated.
    """

    business_user = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='business_reviews', blank=True, null=True)
    reviewer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='customer_reviews', blank=True, null=True)
    rating = models.IntegerField()
    description = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Return a string of the review.

        Returns:
            str: The rating of the review.
        """
        return f"{self.rating}"