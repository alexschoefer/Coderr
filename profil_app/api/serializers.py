from rest_framework import serializers
from profil_app.models import BusinessProfile, CustomerProfile

def get_file_url(user):
    """
    Return the file URL for a user's uploaded file, or None.
    """
    if hasattr(user, 'file') and user.file:
        return user.file.url
    return None

class CustomerProfileSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    created_at = serializers.DateTimeField(source="user.date_joined", read_only=True)
    type = serializers.CharField(source="user.type", read_only=True)
    file = serializers.SerializerMethodField()

    class Meta:
        model = CustomerProfile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "email",
            "created_at",
            "type",
            "file",
        ]

    def get_file(self, obj):
        return get_file_url(obj.user)

class BusinessProfileSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    created_at = serializers.DateTimeField(source="user.date_joined", read_only=True)
    type = serializers.CharField(source="user.type", read_only=True)
    file = serializers.SerializerMethodField()

    class Meta:
        model = BusinessProfile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "email",
            "created_at",
            "type",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
        ]

    def get_file(self, obj):
        return get_file_url(obj.user)