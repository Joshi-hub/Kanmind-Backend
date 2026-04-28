from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import Task, Comment

User = get_user_model()

class UserShortSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(source='get_full_name', read_only=True) 
    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.get_full_name')
    class Meta:
        model = Comment
        fields = ['id', 'created_at', 'author', 'content']

class TaskSerializer(serializers.ModelSerializer):
    assignee = UserShortSerializer(read_only=True)
    reviewer = UserShortSerializer(read_only=True)
    # IDs für POST/PATCH Anfragen
    assignee_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='assignee', write_only=True, required=False, allow_null=True
    )
    reviewer_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='reviewer', write_only=True, required=False, allow_null=True
    )
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id', 'board', 'title', 'description', 'status', 'priority', 
            'assignee', 'reviewer', 'assignee_id', 'reviewer_id', 
            'due_date', 'comments_count'
        ]
        read_only_fields = ['owner']

    def get_comments_count(self, obj):
        return obj.comments.count()