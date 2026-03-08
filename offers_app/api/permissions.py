from rest_framework import permissions


class IsBusinessUser(permissions.BasePermission):
    """
    Custom permission to only allow business users to create offers.
    """

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user and request.user.is_authenticated and request.user.type == 'business'
        
class IsOfferOwner(permissions.BasePermission):
    """
    Custom permission to only allow the owner of an offer to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated and obj.user == request.user
    
class SingleOfferPermission(permissions.BasePermission):
    """
    Custom permission to allow only business users to create offers, and only offer owners to edit or delete them.
    """

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user and request.user.is_authenticated and request.user.type == 'business'
        return True  # Allow GET requests for all authenticated users

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user and request.user.is_authenticated and obj.user == request.user
        return True  # Allow GET requests for all authenticated users