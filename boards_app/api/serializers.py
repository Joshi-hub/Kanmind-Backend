from rest_framework import serializers
from ..models import Board

class BoardPatchSerializer(serializers.ModelSerializer):
    """Serializer for PATCH responses – returns owner_data and members_data as per API spec."""

    title = serializers.CharField(source='name')
    owner_data = serializers.SerializerMethodField()
    members_data = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ['id', 'title', 'owner_data', 'members_data']

    def get_owner_data(self, obj):
        """Return compact owner representation."""
        from user_auth_app.api.serializers import UserShortSerializer
        return UserShortSerializer(obj.owner).data

    def get_members_data(self, obj):
        """Return all members including owner as a flat list."""
        from user_auth_app.api.serializers import UserShortSerializer
        members_list = list(obj.members.all())
        if obj.owner not in members_list:
            members_list.append(obj.owner)
        return UserShortSerializer(members_list, many=True).data


class BoardSerializer(serializers.ModelSerializer):
    """Serializer for GET /api/boards/ and GET /api/boards/{id}/."""

    title = serializers.CharField(source='name')
    owner_id = serializers.ReadOnlyField(source='owner.id')
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    description = serializers.CharField(required=False, allow_blank=True)
    tasks = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = [
            'id', 'title', 'description', 'member_count', 'ticket_count',
            'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id',
            'tasks', 'members',
        ]

    def get_member_count(self, obj):
        """Return total member count including the owner."""

        return obj.members.count()

    def get_ticket_count(self, obj):
        """Return total number of tasks on this board."""

        return obj.tasks.count() if hasattr(obj, 'tasks') else 0

    def get_tasks_to_do_count(self, obj):
        """Return number of tasks with status 'to-do'."""

        if hasattr(obj, 'tasks'):
            return obj.tasks.filter(status='to-do').count()
        return 0

    def get_tasks_high_prio_count(self, obj):
        """Return number of tasks with priority 'high'."""

        if hasattr(obj, 'tasks'):
            return obj.tasks.filter(priority='high').count()
        return 0

    def get_tasks(self, obj):
        """Return serialized list of all tasks belonging to this board."""

        from tasks_app.api.serializers import TaskSerializer
        tasks = obj.tasks.all() if hasattr(obj, 'tasks') else []
        return TaskSerializer(tasks, many=True).data

    def get_members(self, obj):
        """Return serialized member list including the owner."""
        
        from user_auth_app.api.serializers import UserShortSerializer
        members_list = list(obj.members.all())
        if obj.owner not in members_list:
            members_list.append(obj.owner)
        return UserShortSerializer(members_list, many=True).data