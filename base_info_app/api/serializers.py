from rest_framework import serializers
from base_info_app.models import BaseInfo

class BaseInfoSerializer(serializers.Serializer):
    """
    Serializer for BaseInfo model to provide read-only access to aggregated data.
    """

    class Meta:
        model = BaseInfo
        fields = ['review_count', 'average_rating', 'business_profile_count', 'offer_count']
        read_only_fields = ['review_count', 'average_rating', 'business_profile_count', 'offer_count']