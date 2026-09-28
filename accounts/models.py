"""Модели приложения accounts."""
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """Профиль пользователя с дополнительными полями."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь',
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Аватар',
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Телефон',
    )

    class Meta:
        """Метаданные модели."""

        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        """Возвращает имя пользователя."""
        return f'Профиль {self.user.username}'
