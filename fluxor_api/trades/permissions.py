"""
Custom permissions for admin endpoints
"""
from rest_framework import permissions


class IsSuperuserOrStaff(permissions.BasePermission):
    """
    Permission to check if user is superuser OR staff
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.is_superuser or request.user.is_staff)
        )


class IsSuperuser(permissions.BasePermission):
    """
    Permission to check if user is superuser
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_superuser
        )

