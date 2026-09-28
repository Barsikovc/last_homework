"""Настройка админки для приложения accounts."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile


class ProfileInline(admin.StackedInline):
    """Инлайн профиля в админке пользователя."""

    model = Profile
    can_delete = False
    verbose_name_plural = 'Профиль'


class UserAdmin(BaseUserAdmin):
    """Расширенная админка User с профилем."""

    inlines = [ProfileInline]
    list_display = ('id', 'username', 'email', 'is_staff', 'is_active')


# Перерегистрируем User с новым UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Админка для модели Profile."""

    list_display = ('id', 'user', 'phone')
    search_fields = ('user__username', 'phone')
