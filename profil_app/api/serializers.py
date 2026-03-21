from rest_framework import serializers
from profil_app.models import BusinessProfile, CustomerProfile
from upload_app.models import FileUpload

def get_file_url(user):
    """
    Return the file URL for a user's uploaded file, or None.
    """
    if hasattr(user, 'file') and user.file:
        return user.file.url
    return None

class NonNullCharField(serializers.CharField):
    """Custom CharField that returns an empty string instead of None."""
    def to_representation(self, value):
        if value is None:
            return ""
        return super().to_representation(value)

class CustomerProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomerProfile model, including user information and file URL.
    """

    user = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = NonNullCharField(source="user.first_name", read_only=True)
    last_name = NonNullCharField(source="user.last_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    created_at = serializers.DateTimeField(source="user.date_joined", read_only=True)
    file = serializers.SerializerMethodField()
    type = serializers.CharField(source="user.type", read_only=True)
   

    class Meta:
        model = CustomerProfile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "email",
            "created_at",
            "file",
            "type"
        ]

    def get_file(self, obj):
        """Return the file URL for the user's uploaded file, or None if no file exists."""
        return get_file_url(obj.user)

class BusinessProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the BusinessProfile model, including user information and file URL.
    """
    user = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
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
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
            "email",
            "created_at"
        ]

    def get_file(self, obj):
        """Return the file URL for the user's uploaded file, or None if no file exists."""
        return get_file_url(obj.user)
    
class BusinessProfilUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating BusinessProfile information, including user fields.
    """
    first_name = serializers.CharField(source="user.first_name", required=False)
    last_name = serializers.CharField(source="user.last_name", required=False)
    email = serializers.EmailField(source="user.email", required=False)
    file = serializers.FileField(required=False, allow_null=True)
    location = serializers.CharField(required=False, allow_blank=True)
    tel = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    working_hours = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = BusinessProfile
        fields = [
            "first_name",
            "last_name",
            "email",
            "file",
            "location",
            "tel",
            "description",
            "working_hours"
        ]

    def update(self, instance, validated_data):
        """Update the BusinessProfile instance, including related user fields and file upload."""
        user_data = validated_data.pop('user', {})
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        upload_file = validated_data.get('file')
        if upload_file:
            file_upload = FileUpload.objects.create(user=instance.user, file=upload_file)
            instance.user.file = file_upload.file
        instance.user.save()        
        return instance
    

class CustomerProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating CustomerProfile information, including user fields.
    """
    first_name = serializers.CharField(source="user.first_name", required=False, allow_blank=True)
    last_name = serializers.CharField(source="user.last_name", required=False, allow_blank=True)
    email = serializers.EmailField(source="user.email", required=False)
    file = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = CustomerProfile
        fields = [
            "first_name",
            "last_name",
            "email",
            "file"
        ]

    def update(self, instance, validated_data):
        """Update the CustomerProfile instance, including related user fields and file upload."""
        user_data = validated_data.pop('user', {})
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        upload_file = validated_data.get('file')
        if upload_file:
            file_upload = FileUpload.objects.create(user=instance.user, file=upload_file)
            instance.user.file = file_upload.file
        instance.user.save()        
        return instance
    
class BusinessProfilResponseSerializer(serializers.ModelSerializer):
    """
    Serializer for returning BusinessProfile information in responses, including user fields.
    """
    user = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = NonNullCharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    file = serializers.SerializerMethodField()
    location = NonNullCharField(read_only=True)
    tel = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    working_hours = serializers.CharField(read_only=True)
    type = serializers.CharField(source="user.type", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    created_at = serializers.DateTimeField(source="user.date_joined", read_only=True)

    class Meta:
        model = BusinessProfile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
            "email",
            "created_at"
        ]

    def get_file(self, obj):
        """Return the file URL for the user's uploaded file, or None if no file exists."""
        return get_file_url(obj.user)
    
class CustomerProfileResponseSerializer(serializers.ModelSerializer):
    """
    Serializer for returning CustomerProfile information in responses, including user fields.
    """
    user = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    created_at = serializers.DateTimeField(source="user.date_joined", read_only=True)
    type = serializers.CharField(source="user.type", read_only=True)
    file = serializers.SerializerMethodField(required=False, allow_null=True)

    class Meta:
        model = CustomerProfile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "email",
            "type",
            "created_at",
        ]

    def get_file(self, obj):
        """Return the file URL for the user's uploaded file, or None if no file exists."""
        return get_file_url(obj.user)