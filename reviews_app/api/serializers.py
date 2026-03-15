from rest_framework import serializers
from reviews_app.models import Review

class ReviewListSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.
    """

    business_user = serializers.SerializerMethodField(read_only=True)
    reviewer = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 
                  'business_user', 
                  'reviewer', 
                  'rating', 
                  'description', 
                  'created_at', 
                  'updated_at']
    
    def get_reviewer(self, obj):
        """ 
        Returns the ID of the reviewer if it exists, otherwise returns None.
        """
        return obj.reviewer.user.id if obj.reviewer else None
    
    def get_business_user(self, obj):
        """ 
        Returns the ID of the business user if it exists, otherwise returns None.
        """
        return obj.business_user.user.id if obj.business_user else None  
    

class SingleReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for a single Review instance.
    """

    business_user = serializers.SerializerMethodField(read_only=True)
    reviewer = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 
                  'business_user', 
                  'reviewer', 
                  'rating', 
                  'description', 
                  'created_at', 
                  'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def _validation_description(self, value):
        """ 
        Validates the description field to ensure it is at least 50 characters long if it is provided in the initial data.
        """
        if 'description' in self.initial_data:
            description = self.initial_data['description']
            if len(description) > 50:
                raise serializers.ValidationError("Description can only be at least 50 characters long.")
        return value
    
    def get_reviewer(self, obj):
        """ 
        Returns the ID of the reviewer if it exists, otherwise returns None.
        """
        return obj.reviewer.user.id if obj.reviewer else None
    
    def get_business_user(self, obj):
        """ 
        Returns the ID of the business user if it exists, otherwise returns None.
        """
        return obj.business_user.user.id if obj.business_user else None 