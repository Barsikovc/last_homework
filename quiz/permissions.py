from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Чтение — всем, запись — только админам (is_staff)."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsAuthenticatedForAnswer(permissions.BasePermission):
    """Ответ на вопрос — только авторизованным (любым)."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated