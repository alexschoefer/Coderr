from django.db import models

class BaseInfo(models.Model):
    """
    Model to store aggregated base information about reviews, business profiles, and offers.
    """

    review_count = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    business_profile_count = models.IntegerField(default=0)
    offer_count = models.IntegerField(default=0)

    def __str__(self):
        return f"BaseInfo: Reviews={self.review_count}, Average Rating={self.average_rating}, Business Profiles={self.business_profile_count}, Offers={self.offer_count}"