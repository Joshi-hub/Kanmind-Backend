from rest_framework import serializers
from ..models import Board

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('id', 'description', 'name', 'owner')
        read_only_fields = ('id',)
