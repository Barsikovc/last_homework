"""Сериализаторы для приложения catalog."""
from rest_framework import serializers

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        """Метаданные сериализатора."""

        model = Category
        fields = ['id', 'name', 'slug', 'description']


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Product."""

    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        """Метаданные сериализатора."""

        model = Product
        fields = [
            'id', 'category', 'category_name',
            'name', 'description', 'price',
            'image', 'created_at',
        ]
        read_only_fields = ['created_at']
