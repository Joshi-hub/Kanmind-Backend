# tasks_app/admin.py
from django.contrib import admin
from .models import Task, Comment


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'board', 'status', 'priority', 'assignee', 'due_date']
    list_filter = ['status', 'priority']
    search_fields = ['title', 'board__name']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['task', 'author', 'created_at']
    search_fields = ['task__title', 'author__email']