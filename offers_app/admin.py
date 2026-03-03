from django.contrib import admin
from .models import Offer, OfferDetails

# Registriere jedes Modell separat
admin.site.register(Offer)
admin.site.register(OfferDetails)
