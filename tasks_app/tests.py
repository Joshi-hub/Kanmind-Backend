from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.contrib.auth.models import User
from boards_app.models import Board
from tasks_app.models import Task, Comment


class TaskTests(APITestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner@test.com', email='owner@test.com', password='pass1234'
        )
        self.member = User.objects.create_user(
            username='member@test.com', email='member@test.com', password='pass1234'
        )
        self.outsider = User.objects.create_user(
            username='outsider@test.com', email='outsider@test.com', password='pass1234'
        )
        self.owner_token = Token.objects.create(user=self.owner)
        self.member_token = Token.objects.create(user=self.member)
        self.outsider_token = Token.objects.create(user=self.outsider)

        self.board = Board.objects.create(name='Test Board', owner=self.owner)
        self.board.members.add(self.member)

        self.task = Task.objects.create(
            board=self.board,
            title='Test Task',
            owner=self.owner,
            status='to-do',
            priority='medium',
        )
        self.list_url = reverse('task-list-create')
        self.detail_url = reverse('task-detail', args=[self.task.pk])

    def auth(self, token):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    # --- Unauthenticated ---

    def test_get_tasks_unauthenticated_returns_401(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # --- Create ---

    def test_create_task_as_board_member(self):
        self.auth(self.member_token)
        data = {'board': self.board.pk, 'title': 'New Task', 'status': 'to-do', 'priority': 'low'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_task_as_outsider_returns_403(self):
        self.auth(self.outsider_token)
        data = {'board': self.board.pk, 'title': 'Hacked Task', 'status': 'to-do', 'priority': 'low'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --- Update ---

    def test_patch_task_as_member(self):
        self.auth(self.member_token)
        response = self.client.patch(self.detail_url, {'title': 'Updated'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_task_as_outsider_returns_403(self):
        self.auth(self.outsider_token)
        response = self.client.patch(self.detail_url, {'title': 'Hacked'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --- Delete ---

    def test_delete_task_as_owner(self):
        self.auth(self.owner_token)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_task_as_member_returns_403(self):
        self.auth(self.member_token)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --- Assigned/Reviewing filter ---

    def test_assigned_to_me(self):
        self.auth(self.member_token)
        self.task.assignee = self.member
        self.task.save()
        url = reverse('tasks-assigned-to-me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_reviewing(self):
        self.auth(self.member_token)
        self.task.reviewer = self.member
        self.task.save()
        url = reverse('tasks-reviewing')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class CommentTests(APITestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner@test.com', email='owner@test.com', password='pass1234'
        )
        self.outsider = User.objects.create_user(
            username='outsider@test.com', email='outsider@test.com', password='pass1234'
        )
        self.owner_token = Token.objects.create(user=self.owner)
        self.outsider_token = Token.objects.create(user=self.outsider)

        self.board = Board.objects.create(name='Test Board', owner=self.owner)
        self.task = Task.objects.create(
            board=self.board, title='Test Task', owner=self.owner,
            status='to-do', priority='medium',
        )
        self.comment = Comment.objects.create(
            task=self.task, author=self.owner, content='Hello'
        )
        self.list_url = reverse('task-comments', args=[self.task.pk])
        self.delete_url = reverse('task-comment-delete', args=[self.task.pk, self.comment.pk])

    def auth(self, token):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_get_comments_unauthenticated_returns_401(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_comment_as_board_member(self):
        self.auth(self.owner_token)
        response = self.client.post(self.list_url, {'content': 'New comment'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_comment_as_outsider_returns_403(self):
        self.auth(self.outsider_token)
        response = self.client.post(self.list_url, {'content': 'Hacked'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_comment_as_author(self):
        self.auth(self.owner_token)
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_comment_as_outsider_returns_403(self):
        self.auth(self.outsider_token)
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)