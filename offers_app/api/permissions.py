from rest_framework import permissions


class IsBusinessUser(permissions.BasePermission):
    """
    Custom permission to only allow business users to create offers.
    """

    def has_permission(self, request, view):
        """Check if the user is authenticated and is a business user for POST requests, and allow all other requests."""
        if request.method == 'POST':
            return request.user and request.user.is_authenticated and request.user.type == 'business'
        
class IsOfferOwner(permissions.BasePermission):
    """
    Custom permission to only allow the owner of an offer to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        """Check if the user is authenticated and is the owner of the offer."""
        return request.user and request.user.is_authenticated and obj.user == request.user
    
class SingleOfferPermission(permissions.BasePermission):
    """
    Custom permission to allow only business users to create offers, and only offer owners to edit or delete them.
    """

    def has_permission(self, request, view):
        """Check if the user is authenticated and is a business user for POST requests, and allow all other requests."""
        if request.method == 'POST':
            return request.user and request.user.is_authenticated and request.user.type == 'business'
        return True 

    def has_object_permission(self, request, view, obj):
        """ Check if the user is authenticated and is the owner of the offer for PUT, PATCH, and DELETE requests, and allow all other requests."""
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user and request.user.is_authenticated and obj.user == request.user
        return True