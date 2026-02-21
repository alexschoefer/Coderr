from django.db import models

# Imports all settings from core
from django.conf import settings

class CustomerProfile(models.Model):
    """
    Profile for the customer user
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="customer_profile"
    )

    def __str__(self):
        """
        Return a string of the customer profile.

        Returns:
            str: The full name of the customer.
        """
        return f"{self.user.username}"

class BusinessProfile(models.Model):
    """
    Profile for the business user with business specific additional fields
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="business_profile"
    )

    tel = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=255, blank=True)
    description = models.TextField(max_length=255,blank=True)
    working_hours = models.CharField(max_length=20, blank=True)

    def __str__(self):
        """
        Return a string of the business profile.

        Returns:
            str: The full name of the business user.
        """
        return f"{self.user.username}"