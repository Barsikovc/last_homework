"""Настройка админки для приложения reviews."""
from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Админка для модели Review."""

    list_display = ('id', 'user', 'product', 'rating', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved')
    list_editable = ('is_approved',)
    search_fields = ('text',)
