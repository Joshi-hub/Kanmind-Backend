from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.auth.models import User
from boards_app.models import Board


class BoardTests(APITestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner@test.com', email='owner@test.com', password='pass1234'
        )
        self.other = User.objects.create_user(
            username='other@test.com', email='other@test.com', password='pass1234'
        )
        self.owner_token = Token.objects.create(user=self.owner)
        self.other_token = Token.objects.create(user=self.other)
        self.board = Board.objects.create(name='Test Board', owner=self.owner)
        self.list_url = reverse('board-list-create')
        self.detail_url = reverse('board-detail', args=[self.board.pk])

    def auth(self, user_token):
        self.client.credentials(HTTP_AUTHORIZATION='Token' + user_token.key)

    # --- Unauthenticated ---

    def test_get_boards_unauthenticated_returns_401(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_board_unauthenticated_returns_401(self):
        response = self.client.patch(self.detail_url, {'name': 'Updated'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- Authenticated ---

    def test_get_boards_as_owner(self):
        self.auth(self.owner_token)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_board(self):
        self.auth(self.owner_token)
        response = self.client.post(self.list_url, {'title': 'New Board'}, format='json') 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patch_board_as_owner(self):
        self.auth(self.owner_token)
        response = self.client.patch(self.detail_url, {'name': 'Renamed'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_board_as_non_owner_returns_403(self):
        self.auth(self.other_token)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_board_not_member_returns_403(self):
        self.auth(self.other_token)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)