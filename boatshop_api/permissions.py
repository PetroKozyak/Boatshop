from rest_framework import permissions

RETRIEVE_METHOD = "retrieve"
DELETE_METHOD = "destroy"
UPDATE_METHOD = "update"
PATCH_METHOD = "partial_update"


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class HasPermissionForUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user == obj or user.is_superuser or view.action == RETRIEVE_METHOD:
            return True
        else:
            return False


class HasPermissionForOrder(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser or (view.action == RETRIEVE_METHOD and user == obj.boat.owner):
            return True
        elif obj.buyer == user and view.action in [DELETE_METHOD, RETRIEVE_METHOD]:
            return True
        elif obj.boat.owner == user and view.action in [UPDATE_METHOD, PATCH_METHOD]:
            return True
        else:
            return False
