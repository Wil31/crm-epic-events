from rest_framework import permissions


class IsManager(permissions.BasePermission):
    message = "Only Manager authorised"

    def has_permission(self, request, view):
        if request.user.user_type == "MNG":
            return True
        return False
