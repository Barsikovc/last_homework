"""Сериализаторы для приложения reviews."""
from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Review."""

    user = serializers.StringRelatedField(read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        """Метаданные сериализатора."""

        model = Review
        fields = [
            'id', 'user', 'product', 'product_name',
            'text', 'rating', 'is_approved', 'created_at',
        ]
        read_only_fields = ['user', 'is_approved', 'created_at']

    def validate(self, data):
        """Проверяет, что пользователь ещё не оставлял отзыв на этот товар."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            product = data.get('product')
            if product and Review.objects.filter(
                user=request.user, product=product
            ).exists():
                raise serializers.ValidationError(
                    {'product': 'Вы уже оставляли отзыв на этот товар.'}
                )
        return data
