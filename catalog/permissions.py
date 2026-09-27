"""Классы разрешений для приложения catalog."""
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешение: чтение — всем, запись — только админам."""

    def has_permission(self, request, view):
        """Проверяет доступ пользователя к действию."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
