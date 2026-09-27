"""Сериализаторы для приложения quiz."""
from rest_framework import serializers

from .models import Choice, Question, UserAnswer


class ChoiceSerializer(serializers.ModelSerializer):
    """Вариант ответа. is_correct доступен только админу."""

    class Meta:
        """Метаданные сериализатора."""

        model = Choice
        fields = ['id', 'question', 'text', 'is_correct']

    def validate(self, data):
        """Проверяет, что у вопроса только один правильный ответ."""
        is_correct = data.get('is_correct', False)
        question = data.get('question')

        if is_correct and question:
            existing_correct = Choice.objects.filter(
                question=question, is_correct=True
            )
            if self.instance:
                existing_correct = existing_correct.exclude(pk=self.instance.pk)
            if existing_correct.exists():
                raise serializers.ValidationError(
                    {'is_correct': 'У этого вопроса уже есть правильный ответ.'}
                )
        return data


class QuestionSerializer(serializers.ModelSerializer):
    """Вопрос с вариантами (без is_correct — чтобы не спалить ответы)."""

    choices = serializers.SerializerMethodField()

    class Meta:
        """Метаданные сериализатора."""

        model = Question
        fields = ['id', 'product', 'text', 'choices']

    def get_choices(self, obj):
        """Отдаёт варианты без поля is_correct."""
        return [
            {'id': c.id, 'text': c.text}
            for c in obj.choices.all()
        ]


class QuestionAdminSerializer(serializers.ModelSerializer):
    """Сериализатор для админа — с вариантами и is_correct."""

    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        """Метаданные сериализатора."""

        model = Question
        fields = ['id', 'product', 'text', 'choices']


class UserAnswerSerializer(serializers.ModelSerializer):
    """Сериализатор для сохранённых ответов."""

    class Meta:
        """Метаданные сериализатора."""

        model = UserAnswer
        fields = ['id', 'user', 'question', 'choice', 'is_correct', 'created_at']
        read_only_fields = ['user', 'is_correct', 'created_at']
