"""Модели приложения quiz."""
from django.contrib.auth.models import User
from django.db import models

from catalog.models import Product


class Question(models.Model):
    """Тестовый вопрос, привязанный к продукту."""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='Товар',
    )
    text = models.TextField(verbose_name='Текст вопроса')

    class Meta:
        """Метаданные модели."""

        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['id']

    def __str__(self):
        """Возвращает краткое представление вопроса."""
        return f'Вопрос #{self.id}: {self.text[:50]}'


class Choice(models.Model):
    """Вариант ответа на вопрос."""

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices',
        verbose_name='Вопрос',
    )
    text = models.CharField(max_length=255, verbose_name='Текст варианта')
    is_correct = models.BooleanField(default=False, verbose_name='Правильный?')

    class Meta:
        """Метаданные модели."""

        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'
        ordering = ['id']

    def __str__(self):
        """Возвращает текст варианта."""
        return self.text


class UserAnswer(models.Model):
    """Ответ пользователя на вопрос."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Пользователь',
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Вопрос',
    )
    choice = models.ForeignKey(
        Choice,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Выбранный вариант',
    )
    is_correct = models.BooleanField(verbose_name='Правильно?')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата ответа')

    class Meta:
        """Метаданные модели."""

        verbose_name = 'Ответ пользователя'
        verbose_name_plural = 'Ответы пользователей'
        ordering = ['-created_at']

    def __str__(self):
        """Возвращает описание ответа."""
        return f'{self.user.username} — вопрос #{self.question.id}'
