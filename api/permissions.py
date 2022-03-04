from rest_framework import permissions


class ManageOwnProfilePermission(permissions.BasePermission):
    """
    User can only update/delete their own profile
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id
