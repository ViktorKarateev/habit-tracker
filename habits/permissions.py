from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение: доступ разрешён только владельцу объекта.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
