from rest_framework import permissions


class IsOwnerOfReview(permissions.BasePermission):
    """
    Custom permission to only allow the owner of a review to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.reviewer and obj.reviewer.user == request.user
    
class IsAuthenticated(permissions.BasePermission):
    """
    Custom permission to only allow authenticated users to access the view.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
class IsUserAuthorizedToCreateReview(permissions.BasePermission):
    """
    Custom permission to only allow authenticated users to create reviews.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated 
    
    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_authenticated and request.user.type == 'customer'