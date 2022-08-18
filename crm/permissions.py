from rest_framework import permissions


class IsSalesContactOrReadOnly(permissions.BasePermission):
    message = "Only the Sales user can do this action"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.sales_contact == request.user:
            return True
        return False


class IsSalesOrManagerUser(permissions.BasePermission):
    message = "Only the Sales user can do this action"

    def has_permission(
        self,
        request,
        view,
    ):
        if request.user.user_type in ("SLS", "MNG"):
            return True
        return False


class IsStaff(permissions.BasePermission):
    message = "Only staff allowed"

    def has_permission(
        self,
        request,
        view,
    ):
        if request.user.user_type in ("SLS", "MNG", "SPP"):
            return True
        return False
