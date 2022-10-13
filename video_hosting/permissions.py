from rest_framework import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_staff)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.channel == request.user.channel


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        return obj == request.user


class IsAuthenticatedOrOwnerOrReadOnly(IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, permissions.BasePermission):
    pass
