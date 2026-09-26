from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешение:
    - Чтение (GET, HEAD, OPTIONS) — всем.
    - Создание/изменение/удаление — только администраторам (is_staff=True).
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff