from rest_framework import serializers
from orders_app.models import Order
from offers_app.models import Offer, OfferDetails
from profil_app.models import BusinessProfile, CustomerProfile

class OrderListSerializer(serializers.ModelSerializer):

    customer_user = serializers.PrimaryKeyRelatedField(read_only=True)
    business_user = serializers.PrimaryKeyRelatedField(read_only=True)

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

class OrderCreateSerializer(serializers.ModelSerializer):

    offer_detail_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = [
            "offer_detail_id",
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

    def _get_offer_detail(self, offer_detail_id):
        """
        Helper method to retrieve OfferDetail or raise error.
        """
        try:
            return OfferDetails.objects.select_related("offer", "offer__user").get(id=offer_detail_id)
        except OfferDetails.DoesNotExist:
            raise serializers.ValidationError(
                {"offer_detail_id": "OfferDetail with this ID does not exist."}
            )

    def validate(self, attrs):
        """
        Validate the incoming request data.
        """
        offer_detail_id = attrs.get("offer_detail_id")

        if not offer_detail_id:
            raise serializers.ValidationError(
                {"offer_detail_id": "This field is required."}
            )

        offer_detail = self._get_offer_detail(offer_detail_id)

        attrs["offer_detail"] = offer_detail
        return attrs

    def create(self, validated_data):
        """
        Create an Order from the OfferDetail.
        """
        request = self.context["request"]
        offer_detail = validated_data["offer_detail"]

        order = Order.objects.create(
            customer_user=CustomerProfile.objects.get(user=request.user), 
            business_user=BusinessProfile.objects.get(user=offer_detail.offer.user),
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            offer_type=offer_detail.offer_type,
            status="in_progress",
            features=[f for f in offer_detail.features]
        )


        return order