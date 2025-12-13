"""
Custom permissions for the users app.
"""
from rest_framework import permissions


class IsAdminOrSelf(permissions.BasePermission):
    """
    Custom permission to allow:
    - Admin users to access any user's data
    - Authenticated users to access only their own data
    - Anonymous users cannot access
    """

    def has_permission(self, request, view) -> bool:
        """Check if user has permission to access the view."""
        # Must be authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj) -> bool:
        """Check if user has permission to access a specific object."""
        # Admin can access any user
        if request.user.is_staff:
            return True
        # Regular users can only access their own data
        return obj == request.user
