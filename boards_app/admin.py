# boards_app/admin.py
from django.contrib import admin
from .models import Board

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'member_count']
    search_fields = ['name', 'owner__email']

    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Members'