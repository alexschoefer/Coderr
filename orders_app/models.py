from django.db import models
from profil_app.models import CustomerProfile, BusinessProfile
from offers_app.models import Offer, OfferDetails

class Order(models.Model):

    """ 
    Order model to represent an order placed by a customer for a specific offer from a business.
    """

    customer_user = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='customer_profile', blank=True, null=True)
    business_user = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='business_profile', blank=True, null=True)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, blank=True, null=True)
    offer_details = models.ForeignKey(OfferDetails, on_delete=models.CASCADE, blank=True, null=True)

    title = models.CharField(max_length=255)
    revisions = models.IntegerField(default=0)
    delivery_time_in_days = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(null=True, blank=True)
    offer_type = models.CharField(max_length=20)
    status = models.CharField(max_length=20, 
            choices=[
            ('in pogress', 'In Progess'), 
            ('completed', 'Completed'), 
            ('cancelled', 'Cancelled'),
        ],
        default='in pogress'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        String representation of the Order model, showing the order ID and title.
        """
        return f"Order {self.id} - {self.title}"