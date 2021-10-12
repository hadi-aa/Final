from rest_framework import permissions


class IsUserorReadOnly(permissions.BasePermission):
    """
    custom permission to only allow creator of organization to mak change in organization information
    """

    def user_status_ckecker(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        if obj.user == request.user:
            return True
        return False
