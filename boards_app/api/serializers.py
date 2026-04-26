from rest_framework import serializers
from ..models import Board

class BoardSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='name')
    owner_id = serializers.ReadOnlyField(source='owner.id')
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    description = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Board
        fields = [
            'id', 'title', 'description', 'member_count', 'ticket_count', 
            'tasks_to_do_count', 'tasks_high_prio_count', 'owner_id'
        ]

    def get_member_count(self, obj):
        return obj.members.count() + 1

    def get_ticket_count(self, obj):
        return obj.tasks.count() if hasattr(obj, 'tasks') else 0

    def get_tasks_to_do_count(self, obj):
        if hasattr(obj, 'tasks'):
            return obj.tasks.filter(status='to-do').count()
        return 0

    def get_tasks_high_prio_count(self, obj):
        if hasattr(obj, 'tasks'):
            return obj.tasks.filter(priority='high').count() 
        return 0
    