from rest_framework import permissions


class IsUserOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to view/edit the user object
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.username == request.user.username
