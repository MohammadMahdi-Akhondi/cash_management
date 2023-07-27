from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission class that allows access only to the owner of an object or an admin user.
    """

    def has_object_permission(self, request, view, obj):

        if request.user.is_staff or obj.user == request.user:
            return True

        return False
