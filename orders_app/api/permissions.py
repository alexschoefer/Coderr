from rest_framework import permissions

class IsUserCustomer(permissions.BasePermission):
    """
    Custom permission to only allow customers to access certain views.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.type == 'customer'

class IsUserAdmin(permissions.BasePermission):
    """
    Allow access only to admin or staff users.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (request.user.is_staff or request.user.is_superuser)
        )
    
class IsUserBusiness(permissions.BasePermission):
    """
    Custom permission to only allow business users to access certain views.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.type == 'business'
