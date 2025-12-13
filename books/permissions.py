"""
Custom permissions for the books app.
"""
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit objects.
    Read-only permissions are allowed for any request.
    """

    def has_permission(self, request, view) -> bool:
        """Check if user has permission."""
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed for staff users
        return request.user and request.user.is_staff
