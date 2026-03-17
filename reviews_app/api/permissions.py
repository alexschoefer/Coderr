from rest_framework import permissions


class IsOwnerOfReview(permissions.BasePermission):
    """
    Custom permission to only allow the owner of a review to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.reviewer and obj.reviewer.user == request.user
    
class IsUserAuthorizedToCreateReview(permissions.BasePermission):
    """
    Only authenticated users with type 'customer' can create reviews.
    """

    def has_permission(self, request, view):
        return (
            request.user 
            and request.user.is_authenticated 
            and getattr(request.user, "type", None) == "customer"
        )