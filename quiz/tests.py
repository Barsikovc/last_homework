"""Тесты для приложения quiz."""
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from catalog.models import Category, Product
from .models import Choice, Question, UserAnswer


class QuizModelTest(APITestCase):
    """Тесты моделей приложения quiz."""

    def setUp(self):
        """Создаёт тестовые данные."""
        self.cat = Category.objects.create(name='Тест', slug='test')
        self.product = Product.objects.create(
            category=self.cat, name='Товар', price='100.00'
        )
        self.question = Question.objects.create(
            product=self.product, text='Какой цвет у неба?'
        )
        self.correct = Choice.objects.create(
            question=self.question, text='Синий', is_correct=True
        )
        self.wrong = Choice.objects.create(
            question=self.question, text='Зелёный', is_correct=False
        )

    def test_question_str(self):
        """Проверяет строковое представление вопроса."""
        self.assertIn('Какой цвет', str(self.question))

    def test_choice_str(self):
        """Проверяет строковое представление варианта."""
        self.assertEqual(str(self.correct), 'Синий')


class QuizAPITest(APITestCase):
    """Тесты эндпоинтов приложения quiz."""

    def setUp(self):
        """Создаёт пользователя, токен и тестовые данные."""
        self.user = User.objects.create_user(
            username='user1', password='Pass12345'
        )
        self.token = Token.objects.create(user=self.user)

        self.cat = Category.objects.create(name='Тест', slug='test')
        self.product = Product.objects.create(
            category=self.cat, name='Товар', price='100.00'
        )
        self.question = Question.objects.create(
            product=self.product, text='Какой цвет у неба?'
        )
        self.correct = Choice.objects.create(
            question=self.question, text='Синий', is_correct=True
        )
        self.wrong = Choice.objects.create(
            question=self.question, text='Зелёный', is_correct=False
        )

    def test_random_question(self):
        """GET /api/questions/random/ возвращает вопрос без is_correct."""
        response = self.client.get(
            f'/api/questions/random/?product={self.product.id}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.question.id)
        for choice in response.data['choices']:
            self.assertNotIn('is_correct', choice)

    def test_random_question_no_product(self):
        """Без product → 400."""
        response = self.client.get('/api/questions/random/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_answer_without_token(self):
        """Ответ без токена → 401 или 403."""
        response = self.client.post(
            f'/api/questions/{self.question.id}/answer/',
            {'choice': self.correct.id},
            format='json',
        )
        self.assertIn(response.status_code, [
            status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN
        ])

    def test_answer_correct(self):
        """Ответ с правильным choice → correct: true."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(
            f'/api/questions/{self.question.id}/answer/',
            {'choice': self.correct.id},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['correct'])
        self.assertEqual(response.data['correct_choice'], self.correct.id)

    def test_answer_wrong(self):
        """Ответ с неправильным choice → correct: false."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post(
            f'/api/questions/{self.question.id}/answer/',
            {'choice': self.wrong.id},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['correct'])

    def test_user_answer_saved(self):
        """После ответа UserAnswer создаётся в БД."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        self.client.post(
            f'/api/questions/{self.question.id}/answer/',
            {'choice': self.correct.id},
            format='json',
        )
        self.assertTrue(
            UserAnswer.objects.filter(
                user=self.user, question=self.question
            ).exists()
        )
