from rest_framework import serializers

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']


class ProductSerializer(serializers.ModelSerializer):
    # Дополнительно покажем название раздела при чтении
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'category_name',
            'name', 'description', 'price',
            'image', 'created_at',
        ]
        read_only_fields = ['created_at']