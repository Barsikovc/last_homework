"""Настройка админки для приложения users."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Админка для стандартной модели User."""

    pass
