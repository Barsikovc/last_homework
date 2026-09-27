"""Настройка админки для приложения quiz."""
from django.contrib import admin

from .models import Choice, Question, UserAnswer


class ChoiceInline(admin.TabularInline):
    """Инлайн для вариантов ответа."""

    model = Choice
    extra = 2


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Админка для модели Question."""

    list_display = ('id', 'text', 'product')
    list_filter = ('product',)
    inlines = [ChoiceInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    """Админка для модели Choice."""

    list_display = ('id', 'question', 'text', 'is_correct')
    list_filter = ('is_correct',)


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    """Админка для модели UserAnswer."""

    list_display = ('id', 'user', 'question', 'choice', 'is_correct', 'created_at')
    list_filter = ('is_correct',)
