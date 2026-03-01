from rest_framework import serializers
from offers_app.models import Offer, OfferDetails

class OfferDetailsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OfferDetails
        fields = ['id', 'url']
        read_only_fields = ['id', 'url']

class OfferDetailsCreateSerializer(serializers.ModelSerializer):

    features = serializers.ListField(child=serializers.CharField(), required=False)
    
    class Meta:
        model = OfferDetails
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']
        read_only_fields = ['id']
        extra_kwargs = {
            'offer_type': {'required': True}
        }

class OfferCreateSerializer(serializers.ModelSerializer):

    details = OfferDetailsCreateSerializer(source='offer_details', many=True)
    
    class Meta:
        model = Offer
        fields = ['id', 'title', 'description', 'details']
        read_only_fields = ['id']

    def validate_details(self, value):
        """
        Validate that the offer contains at least three details.
        """
        if len(value) > 3:
            raise serializers.ValidationError("An offer must contain at least three details.")
        return value
    
    def create(self, validated_data):
        """
        Create an offer along with its details. The details are expected to be provided in the 'details' field of the input data.
        """
        details_data = validated_data.pop('offer_details', [])  # Match the source name

        offer = Offer.objects.create(**validated_data)

        for detail_data in details_data:
            features = detail_data.pop('features', [])
            offer_detail = OfferDetails.objects.create(offer=offer, **detail_data)
            offer_detail.features = features
            offer_detail.save()
        return offer

