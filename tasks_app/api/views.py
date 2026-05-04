from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import Task, Comment
from .serializers import TaskSerializer, CommentSerializer
from .permissions import IsBoardMember, IsTaskOwnerOrBoardOwner, IsBoardMemberForComment, IsCommentAuthor


class AssignedToMeTaskListView(generics.ListAPIView):
    """Return all tasks where the authenticated user is the assignee."""

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter tasks by the current user as assignee."""
        return Task.objects.filter(assignee=self.request.user)


class ReviewingTaskListView(generics.ListAPIView):
    """Return all tasks where the authenticated user is the reviewer."""

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter tasks by the current user as reviewer."""
        return Task.objects.filter(reviewer=self.request.user)


class TaskListCreateView(generics.ListCreateAPIView):
    """List all tasks or create a new task within a board."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsBoardMember]

    def list(self, request, *args, **kwargs):
        """Return all tasks."""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """Save the task with the current user as owner."""
        serializer.save(owner=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a single task."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsTaskOwnerOrBoardOwner]


class TaskCommentListCreateView(generics.ListCreateAPIView):
    """List all comments for a task or create a new one."""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsBoardMemberForComment]

    def get_queryset(self):
        """Return comments for the task specified in the URL, or 404 if task not found."""
        get_object_or_404(Task, id=self.kwargs['task_id'])
        return Comment.objects.filter(task_id=self.kwargs['task_id'])

    def perform_create(self, serializer):
        """Save the comment with the current user as author."""
        task = get_object_or_404(Task, id=self.kwargs['task_id'])
        serializer.save(author=self.request.user, task=task)


class CommentDestroyView(generics.DestroyAPIView):
    """Delete a single comment – only the comment's author may do so."""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsBoardMemberForComment, IsCommentAuthor]

    def get_object(self):
        """Return the comment, ensuring it belongs to the correct task."""
        get_object_or_404(Task, id=self.kwargs['task_id'])
        comment = get_object_or_404(
            Comment,
            id=self.kwargs['comment_id'],
            task_id=self.kwargs['task_id'],
        )
        self.check_object_permissions(self.request, comment)
        return comment