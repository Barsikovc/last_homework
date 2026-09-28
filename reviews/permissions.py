"""Классы разрешений для приложения reviews."""
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Разрешение: редактировать/удалять может только автор или админ."""

    def has_object_permission(self, request, view, obj):
        """Проверяет права на объект."""
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user and request.user.is_staff:
            return True
        return obj.user == request.user


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """Разрешение: создавать может только авторизованный, читать — все."""

    def has_permission(self, request, view):
        """Проверяет права на действие."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated
