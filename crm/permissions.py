from rest_framework import permissions


class IsSalesOrManagerOrReadOnly(permissions.BasePermission):
    message = "Only authorised users (Sales, Manager) can do this action"

    def has_permission(self, request, view):
        if (
            request.method not in permissions.SAFE_METHODS
            and request.user.user_type not in ("SLS", "MNG")
        ):
            return False
        return True


class IsClientSalesContactOrReadOnly(permissions.BasePermission):
    message = "Only the Sales contact or Manager can do this action"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.user_type == "MNG":
            return True
        if obj.sales_contact == request.user:
            return True
        return False


class IsContractSalesContactOrReadOnly(permissions.BasePermission):
    message = "Only the client Sales contact or Manager can do this action"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.user_type == "MNG":
            return True
        if obj.client.sales_contact == request.user:
            return True
        return False


class IsSupportContactOrSalesOrReadOnly(permissions.BasePermission):
    message = "Only authorised users can do this action"

    def has_object_permission(self, request, view, obj):
        if view.action == "update" and obj.support_contact == request.user:
            return True
        if obj.client.sales_contact == request.user:
            return True
        if request.user.user_type == "MNG":
            return True
        return False


class IsStaff(permissions.BasePermission):
    message = "Only staff allowed"

    def has_permission(self, request, view):
        if request.user.user_type in ("SLS", "MNG", "SPP"):
            return True
        return False
