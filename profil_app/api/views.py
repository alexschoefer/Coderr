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
from profil_app.api.serializers import BusinessProfileSerializer, CustomerProfileSerializer, BusinessProfilUpdateSerializer, CustomerProfileUpdateSerializer, CustomerProfileResponseSerializer, BusinessProfilResponseSerializer


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
        user_obj = get_object_or_404(CustomUser, pk=pk)

        profile = self._get_profile(user_obj)

        serializer = self._get_detail_serializer(profile)
        return Response(serializer.data)

    def patch(self, request, pk=None):
        """
        Update a specific profile by user ID.
        """
        user_obj = get_object_or_404(CustomUser, pk=pk)

        if request.user != user_obj:
            return Response({"detail": "You do not have permission to update this profile."}, status=status.HTTP_403_FORBIDDEN)

        profile = self._get_profile(user_obj)

        serializer = self._get_update_serializer(profile, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            response_serializer = self._get_detail_serializer(profile)
            return Response(response_serializer.data)
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
        Return the appropriate serializer instance based on the profile type.
        """
        if data is not None:
            if isinstance(profile, BusinessProfile):
                return BusinessProfilUpdateSerializer(profile, data=data, partial=partial)
            elif isinstance(profile, CustomerProfile):
                return CustomerProfileUpdateSerializer(profile, data=data, partial=partial)
        else:
            if isinstance(profile, CustomerProfile):
                return CustomerProfileSerializer(profile)
            elif isinstance(profile, BusinessProfile):
                return BusinessProfilResponseSerializer(profile)
    
    def _get_update_serializer(self, profile, data):
        """
        Return the appropriate serializer instance for updating based on the profile type.
        """
        if isinstance(profile, BusinessProfile):
            return BusinessProfilUpdateSerializer(profile, data=data, partial=True)
        elif isinstance(profile, CustomerProfile):
            return CustomerProfileUpdateSerializer(profile, data=data, partial=True)

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