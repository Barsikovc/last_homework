from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения данных пользователя."""

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации нового пользователя."""

    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm']

        def validate(self, data):
            """Проверяет совпадение пароля и подтверждения."""
            if data['password'] != data['password_confirm']:
                raise serializers.ValidationError({"password": "Пароли не совпадают."})
            return data

        def create(self, validated_data):
            """Создаёт нового пользователя."""
            validated_data.pop('password_confirm')
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data.get('email', ''),
                password=validated_data['password'],
            )
            return user
