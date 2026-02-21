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

# class UserProfileView(generics.RetrieveUpdateAPIView):
#     """
#     API view to retrieve or update a user profile (customer or business) by UserID.
#     """
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [TokenAuthentication]

#     def get_object(self):
#         """
#         Retrieve the profile (CustomerProfile or BusinessProfile) based on the UserID.
#         """
#         user_id = self.kwargs.get('pk')
#         try:
#             if CustomerProfile.objects.filter(user_id=user_id).exists():
#                 return CustomerProfile.objects.get(user_id=user_id)
#             elif BusinessProfile.objects.filter(user_id=user_id).exists():
#                 return BusinessProfile.objects.get(user_id=user_id)
#         except (CustomerProfile.DoesNotExist, BusinessProfile.DoesNotExist):
#             raise Http404("Profile not found for the given UserID.")
#         raise Http404("Profile not found for the given UserID.")

#     def get_serializer_class(self):
#         """
#         Dynamically return the serializer class based on the profile type.
#         """
#         profile = self.get_object()
#         if isinstance(profile, CustomerProfile):
#             return CustomerProfileSerializer
#         elif isinstance(profile, BusinessProfile):
#             return BusinessProfileSerializer
#         raise ValueError("Invalid profile type.")


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
    Retrieve a specific profile (customer or business) by user ID.
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

    def _get_profile(self, user_obj):
        """
        Retrieve the associated profile (CustomerProfile or BusinessProfile) for the user.
        """
        if user_obj.type == 'customer':
            return get_object_or_404(CustomerProfile, user=user_obj)
        elif user_obj.type == 'business':
            return get_object_or_404(BusinessProfile, user=user_obj)
        raise Http404("Profile not found for the given user type.")

    def _get_detail_serializer(self, profile):
        """
        Return the appropriate serializer for the profile.
        """
        if isinstance(profile, CustomerProfile):
            return CustomerProfileSerializer(profile)
        elif isinstance(profile, BusinessProfile):
            return BusinessProfileSerializer(profile)
        raise ValueError("Invalid profile type.")