from rest_framework import serializers
from offers_app.models import Offer, OfferDetails
from profil_app.models import CustomerProfile, BusinessProfile
from upload_app.models import FileUpload


class OfferDetailsSerializer(serializers.ModelSerializer):

    url = serializers.SerializerMethodField()
    
    class Meta:
        model = OfferDetails
        fields = ['id', 'url']
        read_only_fields = ['id', 'url']
    
    def get_url(self, obj):
            return f"/api/offers/{obj.offer.id}/details/{obj.id}/"

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
        details_data = validated_data.pop('offer_details', [])
        uploaded_image = validated_data.pop('image', None)

        if uploaded_image:
            file_upload = FileUpload.objects.create(file=uploaded_image)
            validated_data['image'] = file_upload

        offer = Offer.objects.create(**validated_data)

        for detail_data in details_data:
            features = detail_data.pop('features', [])
            offer_detail = OfferDetails.objects.create(offer=offer, **detail_data)
            offer_detail.features = features
            offer_detail.save()
        return offer
    

class UserDetailsSerializer(serializers.Serializer):
        
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()


class OfferListSerializer(serializers.ModelSerializer):

    details = OfferDetailsSerializer(source='offer_details', many=True, read_only=True)
    user_details = UserDetailsSerializer(source='user', read_only=True)
    image = serializers.SerializerMethodField()

    min_price = serializers.DecimalField(
    source="annotated_min_price",
    max_digits=10,
    decimal_places=2,
    read_only=True
    )

    min_delivery_time = serializers.IntegerField(
    source="annotated_min_delivery_time",
    read_only=True
    )

    class Meta:
        model = Offer
        fields = [
            'id',
            'user',
            'title',
            'image',
            'description',
            'created_at',
            'updated_at',
            'details',
            'min_price',
            'min_delivery_time',
            'user_details'
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'min_price',
            'min_delivery_time',
            'user_details',
            'details'
        ]

    def get_image(self, obj):
        """
        Return the full URL of the image if it exists, otherwise return None.
        """
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

class SingleOfferDetailSerializer(serializers.ModelSerializer):

    """Serializer for retrieving a single offer detail."""

    details = OfferDetailsSerializer(source='offer_details', many=True, read_only=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = [
            'id',
            'user',
            'title',
            'image',
            'description',
            'created_at',
            'updated_at',
            'details',
            'min_price',
            'min_delivery_time'
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
            'min_price',
            'min_delivery_time',
            'details'
        ]
    
    def get_image(self, obj):
        """
        Return the full URL of the image if it exists, otherwise return None.
        """
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None