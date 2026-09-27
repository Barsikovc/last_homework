"""Настройка админки для приложения catalog."""
from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка для модели Category."""

    list_display = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админка для модели Product."""

    list_display = ('id', 'name', 'category', 'price', 'created_at')
    list_filter = ('category',)
    search_fields = ('name',)
