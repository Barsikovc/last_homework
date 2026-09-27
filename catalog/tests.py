"""Тесты для приложения catalog."""
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Category


class CategoryModelTest(APITestCase):
    """Тесты модели Category."""

    def test_create_category(self):
        """Проверяет создание категории."""
        cat = Category.objects.create(name='Тест', slug='test')
        self.assertEqual(cat.name, 'Тест')
        self.assertEqual(str(cat), 'Тест')


class CatalogAPITest(APITestCase):
    """Тесты эндпоинтов приложения catalog."""

    def setUp(self):
        """Создаёт админа, токен и категорию для тестов."""
        self.admin = User.objects.create_superuser(
            username='admin', password='Admin12345'
        )
        self.token = Token.objects.create(user=self.admin)
        self.category = Category.objects.create(
            name='Электроника', slug='electronics'
        )

    def test_list_categories_anonymous(self):
        """GET доступен всем."""
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)

    def test_create_category_without_token(self):
        """POST без токена → 401 или 403."""
        response = self.client.post('/api/categories/', {
            'name': 'Спорт', 'slug': 'sport'
        }, format='json')
        self.assertIn(response.status_code, [
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN,
        ])

    def test_create_category_with_token(self):
        """POST с токеном админа → 201."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post('/api/categories/', {
            'name': 'Спорт', 'slug': 'sport'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_category(self):
        """PATCH обновляет категорию."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.patch(
            f'/api/categories/{self.category.id}/',
            {'description': 'Новое'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_category(self):
        """DELETE удаляет категорию."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.delete(f'/api/categories/{self.category.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_product(self):
        """POST создаёт товар."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post('/api/products/', {
            'category': self.category.id,
            'name': 'Смартфон',
            'price': '29999.00',
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
