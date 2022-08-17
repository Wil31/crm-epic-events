from rest_framework.permissions import BasePermission
from rest_framework import permissions


# class IsSalesAuthenticated(BasePermission):
#     def has_permission(self, request, view):
#         return bool(
#             request.user
#             and request.user.is_authenticated
#             and request.user.user_type == "SLS"
#         )


class IsSalesContactOfClient(BasePermission):
    message = "Only the Sales user can do this action"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.sales_contact == request.user
