from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class UserModelTest(APITestCase):
    """Тесты модели User."""

    def test_create_user(self):
        user = User.objects.create_user(username='test', password='Pass12345')
        self.assertEqual(user.username, 'test')
        self.assertTrue(user.check_password('Pass12345'))
        self.assertFalse(user.is_staff)

    def test_str(self):
        user = User.objects.create_user(username='test', password='Pass12345')
        self.assertEqual(str(user), 'test')


class UserAPITest(APITestCase):
    """Тесты эндпоинтов users."""

    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='admin', password='Admin12345', email='admin@test.com'
        )
        self.token = Token.objects.create(user=self.admin)

    def test_list_users_anonymous(self):
        """GET /api/users/ доступен без токена."""
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_user(self):
        """POST /api/users/register/ создаёт пользователя."""
        data = {
            'username': 'newuser',
            'email': 'new@test.com',
            'password': 'NewPass123',
            'password_confirm': 'NewPass123',
        }
        response = self.client.post('/api/users/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_password_mismatch(self):
        """Пароли не совпадают → 400."""
        data = {
            'username': 'newuser',
            'password': 'Pass12345',
            'password_confirm': 'Other12345',
        }
        response = self.client.post('/api/users/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TokenTest(APITestCase):
    """Тесты получения токена."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='admin', password='Admin12345'
        )

    def test_obtain_token(self):
        response = self.client.post('/api/token/', {
            'username': 'admin',
            'password': 'Admin12345',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)