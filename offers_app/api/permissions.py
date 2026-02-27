from rest_framework import permissions


class IsBusinessUser(permissions.BasePermission):
    """
    Custom permission to only allow business users to create offers.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and is a business user
        return request.user and request.user.is_authenticated and request.user.is_business