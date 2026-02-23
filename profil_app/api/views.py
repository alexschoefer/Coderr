from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.http import Http404
from django.shortcuts import get_object_or_404

from auth_app.models import CustomUser
from profil_app.models import BusinessProfile, CustomerProfile
from profil_app.api.serializers import BusinessProfileSerializer, CustomerProfileSerializer


class BusinessProfileDetailView(generics.RetrieveAPIView):
    """
    Retrieve a specific business profile by the given ID.
    """

    queryset = BusinessProfile.objects.all()
    serializer_class = BusinessProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    lookup_field = 'pk'


class UserProfileView(APIView):
    """
    Retrieve or update a specific profile (customer or business) by user ID.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, pk=None):
        """
        Retrieve a specific profile by user ID.
        """
        # Retrieve the user object
        user_obj = get_object_or_404(CustomUser, pk=pk)

        # Determine the profile type and retrieve the profile
        profile = self._get_profile(user_obj)

        # Serialize the profile data
        serializer = self._get_detail_serializer(profile)
        return Response(serializer.data)

    def patch(self, request, pk=None):
        """
        Update a specific profile by user ID.
        """
        # Retrieve the user object
        user_obj = get_object_or_404(CustomUser, pk=pk)

        # Check if the authenticated user is the owner of the profile
        if request.user != user_obj:
            return Response({"detail": "You do not have permission to update this profile."}, status=status.HTTP_403_FORBIDDEN)

        # Determine the profile type and retrieve the profile
        profile = self._get_profile(user_obj)

        # Serialize the profile data with the incoming request data
        serializer = self._get_detail_serializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _get_profile(self, user_obj):
        """
        Retrieve the associated profile (CustomerProfile or BusinessProfile) for the user.
        """
        if user_obj.type == 'customer':
            return get_object_or_404(CustomerProfile, user=user_obj)
        elif user_obj.type == 'business':
            return get_object_or_404(BusinessProfile, user=user_obj)
        raise Http404("Profile not found for the given user type.")

    def _get_detail_serializer(self, profile, data=None, partial=False):
        """
        Return the appropriate serializer for the profile.
        """
        if isinstance(profile, CustomerProfile):
            return CustomerProfileSerializer(profile, data=data, partial=partial)
        elif isinstance(profile, BusinessProfile):
            return BusinessProfileSerializer(profile, data=data, partial=partial)
        raise ValueError("Invalid profile type.")
    

class BusinessProfileListView(generics.ListAPIView):
    """
    List all business profiles.
    """
    queryset = BusinessProfile.objects.all()
    serializer_class = BusinessProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class CustomerProfileListView(generics.ListAPIView):
    """
    List all customer profiles.
    """
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]