from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Question, Choice, UserAnswer
from .permissions import IsAdminOrReadOnly, IsAuthenticatedForAnswer
from .serializers import (
    QuestionSerializer,
    QuestionAdminSerializer,
    ChoiceSerializer,
    UserAnswerSerializer,
)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None  # без пагинации, чтобы удобно было в тестах

    def get_serializer_class(self):
        # Админ видит is_correct, остальные — нет
        if self.request.user and self.request.user.is_staff:
            return QuestionAdminSerializer
        return QuestionSerializer

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def random(self, request):
        """
        GET /api/questions/random/?product=<id>
        Возвращает случайный вопрос по продукту.
        """
        product_id = request.query_params.get('product')
        if not product_id:
            return Response(
                {'detail': 'Параметр product обязателен.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        question = Question.objects.filter(product_id=product_id).order_by('?').first()
        if not question:
            return Response(
                {'detail': 'Вопросов для этого продукта нет.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = QuestionSerializer(question, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticatedForAnswer])
    def answer(self, request, pk=None):
        """
        POST /api/questions/<id>/answer/
        Тело: {"choice": <id>}
        Ответ: {"correct": true/false, "correct_choice": <id>}
        """
        question = self.get_object()
        choice_id = request.data.get('choice')

        if not choice_id:
            return Response(
                {'detail': 'Поле choice обязательно.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        choice = get_object_or_404(Choice, pk=choice_id, question=question)
        is_correct = choice.is_correct

        UserAnswer.objects.create(
            user=request.user,
            question=question,
            choice=choice,
            is_correct=is_correct,
        )

        correct_choice = question.choices.filter(is_correct=True).first()

        return Response({
            'correct': is_correct,
            'correct_choice': correct_choice.id if correct_choice else None,
        })


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [IsAdminOrReadOnly]


class UserAnswerViewSet(viewsets.ReadOnlyModelViewSet):
    """Только просмотр своих ответов. Создание — через /questions/{id}/answer/."""
    serializer_class = UserAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserAnswer.objects.filter(user=self.request.user)