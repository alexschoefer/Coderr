from rest_framework import serializers
from offers_app.models import Offer, OfferDetails
from profil_app.models import CustomerProfile, BusinessProfile
from upload_app.models import FileUpload
from django.db.models import Min
from django.urls import reverse

def get_image_url(offer):
    """
    Helper-function - Return the file URL for an offer's uploaded image, or None.
    """
    if offer.image and offer.image.file:
        return offer.image.file.url
    return ""

class OfferDetailsListSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving offer details. The 'url' field provides a link to the detail view of the offer detail instance.
    """

    url = serializers.SerializerMethodField()
    
    class Meta:
        model = OfferDetails
        fields = ['id', 'url']
        read_only_fields = ['id', 'url']
    
    def get_url(self, obj):
        """Return the URL for the offer detail instance."""
        return f"/offerdetails/{obj.id}/"
    
class OfferDetailsSerializer(serializers.ModelSerializer):
    """Serializer for retrieving offer details. The 'url' field provides a link to the detail view of the offer detail instance."""
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = OfferDetails
        fields = ['id', 'url']
        read_only_fields = ['id', 'url']
    
    def get_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(f"/api/offerdetails/{obj.id}/")

class OfferDetailsCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating offer details. 
    This serializer includes fields for the offer detail's title, revisions, delivery time, price, features, and offer type. 
    The 'features' field is a list of strings that can be provided when creating or updating an offer detail.
    """
    features = serializers.ListField(child=serializers.CharField(), required=False)
    
    class Meta:
        model = OfferDetails
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']
        read_only_fields = ['id']
        extra_kwargs = {
            'offer_type': {'required': True}
        }

class OfferCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating offers. This serializer includes fields for the offer's title, description, and an optional image.
    """
    details = OfferDetailsCreateSerializer(source='offer_details', many=True)
    image = serializers.FileField(required=False, allow_null=True)
    
    class Meta:
        model = Offer
        fields = ['id', 'title', 'image','description', 'details']
        read_only_fields = ['id']

    def validate_details(self, value):
        """
        Validate that the offer contains at least three details.
        """
        if len(value) < 3:
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
    """
    Serializer for retrieving user details associated with an offer. This serializer includes the user's first name, last name, and username.
    """
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()


class OfferListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing offers with their details and associated user information.
    """
    details = OfferDetailsListSerializer(source='offer_details', many=True, read_only=True)
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

class SingleOfferSerializer(serializers.ModelSerializer):
    """Serializer for retrieving a single offer detail."""

    details = OfferDetailsSerializer(source='offer_details', many=True, read_only=True)
    image = serializers.SerializerMethodField()
    min_price = serializers.SerializerMethodField()
    min_delivery_time = serializers.SerializerMethodField()

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
            """Return the file URL for the offer's image, or None."""
            return get_image_url(obj)

    def get_min_price(self, obj):
            """
            Return the minimum price for the offer. If the offer has a min_price field set, return that value. 
            Otherwise, calculate the minimum price from the offer details. 
            If there are no offer details, return 0.
            """
            if obj.min_price is not None:
                return obj.min_price
            if obj.offer_details.exists():
                return obj.offer_details.aggregate(Min('price'))['price__min'] or 0
            return 0

    def get_min_delivery_time(self, obj):
            """
            Return the minimum delivery time for the offer. If the offer has a min_delivery_time field set, return that value.
            """
            if obj.min_delivery_time is not None:
                return obj.min_delivery_time
            if obj.offer_details.exists():
                    return obj.offer_details.aggregate(Min('delivery_time_in_days'))['delivery_time_in_days__min'] or 0
            return 0
                     
class SingleUpdateOfferSerializer(serializers.ModelSerializer):

    """Serializer for updating a single offer."""

    details = OfferDetailsCreateSerializer(source='offer_details', many=True)
    image = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Offer
        fields = [
            'id',
            'title',
            'image', 
            'description',
            'details',
        ]
        read_only_fields = [
            'id'
        ]

    def validate(self, attrs):
        """
        Validate that each offer detail includes an 'offer_type' field.
        """

        details_data = self.initial_data.get('details', [])
        if details_data:
            for detail in details_data:
                if 'offer_type' not in detail:
                    raise serializers.ValidationError("Each offer detail must include an 'offer_type'.")
        return attrs

    def _update_or_create_offer_details(self, instance, details_data):
        """
        Update existing offer details or create new ones based on the provided data. The 'offer_type' field is used to identify existing details.
        """

        for detail_data in details_data:
            offer_type = detail_data.get('offer_type')
            if offer_type:
                try:
                    detail = instance.offer_details.get(offer_type=offer_type)
                    for attr, value in detail_data.items():
                        setattr(detail, attr, value)
                    detail.save()
                except OfferDetails.DoesNotExist:
                    OfferDetails.objects.create(offer=instance, **detail_data)
                
    def _recalculate_min_price_and_delivery_time(self, instance):

        """
        Recalculate the minimum price and delivery time for the offer based on its details. 
        This should be called after updating or creating offer details to ensure that the offer's min_price and min_delivery_time fields are accurate.
        """

        details = instance.offer_details.all()
        instance.min_price = min((detail.price for detail in details), default=None)
        instance.min_delivery_time = min((detail.delivery_time_in_days for detail in details), default=None)
        instance.save()

    def _update_basic_offer_fields(self, instance, validated_data):

        """
        Update the basic fields of the offer (title, description, and image) based on the provided validated data. 
        The image is handled separately to allow for file uploads, and the title and description are updated directly from the validated data.
        """

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)

        uploaded_image = validated_data.pop('image', None)

        if uploaded_image:
            file_upload = FileUpload.objects.create(file=uploaded_image)
            instance.image = file_upload

        for attr, value in validated_data.items():
            if attr != 'offer_details':
                setattr(instance, attr, value)
        instance.save()
    
    def update(self, instance, validated_data):

        """
        Update an offer instance with the provided validated data. 
        This method handles updating the basic fields of the offer, as well as updating or creating offer details based on the provided details data. 
        After updating the details, it recalculates the minimum price and delivery time for the offer to ensure that these fields are accurate.
        """

        self._update_basic_offer_fields(instance, validated_data)
        details_data = validated_data.get('offer_details', [])
        if details_data:
            self._update_or_create_offer_details(instance, details_data)
            self._recalculate_min_price_and_delivery_time(instance)
        instance.refresh_from_db() 
        return instance
    
class SingleDeleteOfferSerializer(serializers.ModelSerializer):

    """Serializer for deleting a single offer."""

    class Meta:
        model = Offer
        fields = ['id']
        read_only_fields = ['id']

class SingleDetailOfferSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OfferDetails
        fields = [
            'id', 
            'title', 
            'revisions', 
            'delivery_time_in_days', 
            'price', 
            'features', 
            'offer_type'
            ]