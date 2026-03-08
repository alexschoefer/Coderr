from rest_framework import serializers
from orders_app.models import Order
from offers_app.models import Offer, OfferDetails

class OrderListSerializer(serializers.ModelSerializer):

    customer_user = serializers.StringRelatedField()
    business_user = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at"
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at"
        ]

