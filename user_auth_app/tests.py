from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.auth.models import User


class AuthTests(APITestCase):

    def setUp(self): 
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user = User.objects.create_user(  
            username='test@test.com',
            email='test@test.com',
            password='testpass123',
            first_name='Test',
            last_name='User',
        )
        self.token = Token.objects.create(user=self.user)

    # --- Registration ---

    def test_registration_success(self):
        data = {
            'email': 'new@test.com',
            'password': 'newpass123',
            'repeated_password': 'newpass123',
            'fullname': 'New User',
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)

    def test_registration_passwords_dont_match(self):
        data = {
            'email': 'new@test.com',
            'password': 'newpass123',
            'repeated_password': 'different',
            'fullname': 'New User',
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_duplicate_email(self):
        data = {
            'email': 'test@test.com', 
            'password': 'newpass123',
            'repeated_password': 'newpass123',
            'fullname': 'New User',
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_password_too_short(self):
        data = {
            'email': 'short@test.com',
            'password': '123',
            'repeated_password': '123',
            'fullname': 'Short Pass',
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # --- Login ---

    def test_login_success(self):
        data = {'email': 'test@test.com', 'password': 'testpass123'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_wrong_password(self):
        data = {'email': 'test@test.com', 'password': 'wrongpass'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_email_not_found(self):
        data = {'email': 'nobody@test.com', 'password': 'testpass123'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # --- Unauthenticated ---

    def test_unauthenticated_request_returns_401(self):
        url = reverse('board-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)