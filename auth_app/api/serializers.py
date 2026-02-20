from rest_framework import serializers
from auth_app.models import CustomUser
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import authenticate

class RegistrationSerializer(serializers.ModelSerializer):

    """
    Serializer for user registration.

    Handles validation of email uniqueness, password confirmation
    and creation of the User and related UserProfile.
    """
    repeated_password = serializers.CharField(write_only=True)
    fullname = serializers.CharField(write_only=True)

    class Meta:
        model = AbstractUser
        fields = [
            'email', 
            'fullname', 
            'password', 
            'repeated_password',
            'type']
        extra_kwargs = {
            "password": {"write_only": True}
        }
    
    def validate(self, data):
        """
        Validate that password and repeated_password match.

        :param data: Incoming validated data
        :return: Validated data
        :raises ValidationError: If passwords do not match
        """
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({"password": "Your passwords do not match. Please try again."})
        return data
    
    def validate_email(self, value):
        """
        Validate that the email address is unique.

        :param value: Email address
        :return: Email address
        :raises ValidationError: If email already exists
        """
        if AbstractUser.objects.filter(email=value).exists():
            raise serializers.ValidationError('The email address already belongs to an account.')
        return value

    def create(self, validated_data):
        """
        Create a new user and associated user profile.

        :param validated_data: Validated serializer data
        :return: Created User instance
        """
        validated_data.pop('repeated_password')
        fullname = validated_data.pop('fullname')
        email = validated_data['email']

        user = AbstractUser.objects.create_user(
            username=fullname,
            email=email,
            password=validated_data['password']
        )
        CustomUser.objects.create(user=user, fullname=fullname)
        return user