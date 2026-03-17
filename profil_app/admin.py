from django.contrib import admin
from .models import CustomerProfile, BusinessProfile

# Register your models here.
admin.site.register(CustomerProfile),
admin.site.register(BusinessProfile)