from django.contrib.auth import get_user_model
from rest_framework import serializers
from ..models import Task, Comment
from user_auth_app.api.serializers import UserShortSerializer

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    """Serialize a Comment, always returning a two-word author name for JS initials."""

    author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']

    def get_author(self, obj):
        """Return full name with guaranteed two words to prevent getInitials() crash."""
        name = f"{obj.author.first_name} {obj.author.last_name}".strip() or obj.author.username
        if ' ' not in name:
            return f"{name} {name}"
        return name


class TaskSerializer(serializers.ModelSerializer):
    """Serialize a Task with nested user objects for assignee, reviewer, and owner."""

    assignee = UserShortSerializer(read_only=True)
    reviewer = UserShortSerializer(read_only=True)
    owner = UserShortSerializer(read_only=True)

    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='assignee',
        write_only=True, required=False, allow_null=True,
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='reviewer',
        write_only=True, required=False, allow_null=True,
    )
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'board', 'title', 'description', 'status', 'priority',
            'assignee', 'reviewer', 'owner',
            'assignee_id', 'reviewer_id',
            'due_date', 'comments_count',
        ]
        read_only_fields = ['owner']

    def get_comments_count(self, obj):
        """Return the total number of comments for this task."""
        return obj.comments.count()