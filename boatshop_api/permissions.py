from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class HasPermissionForUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser or user == obj or view.action == "retrieve":
            return True
        else:
            return False


class HasPermissionForOrder(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        if obj.buyer == user:
            return True
        elif obj.boat.owner == user:
            return True
        elif view.action == "retrieve":
            return True
        else:
            return False


