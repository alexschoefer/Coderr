from rest_framework import serializers
from offers_app.models import Offer, OfferDetails

class OfferDetailsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OfferDetails
        fields = ['id', 'url']
        read_only_fields = ['id', 'url']

class OfferCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Offer
        fields = ['id', 'image','title', 'description', 'min_price', 'min_delivery_time']
        read_only_fields = ['id']

    """
    Validate that the offer contains at least three details.
    """

    def validate_details(self, value):

        if len(value) > 3:
            raise serializers.ValidationError("An offer must contain at least three details.")
        return value
    
    def create(self, validated_data):
        
        details_data = validated_data.pop('details', [])

        offer = Offer.objects.create(**validated_data)

        for detail_data in details_data:
            features = detail_data.pop('features', [])
            offer_detail = OfferDetails.objects.create(offer=offer, **detail_data)
            offer_detail.features = features
            offer_detail.save()
        return offer

class OfferDetailsCreateSerializer(serializers.ModelSerializer):

    feature = serializers.ListField(child=serializers.CharField(), required=False)
    
    class Meta:
        model = OfferDetails
        fields = ['id', 'offer', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']
        read_only_fields = ['id']
        extra_kwargs = {
            'offer': {'required': True}
        }