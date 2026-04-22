from django.urls import path
from .views import TaskList, TasksAssignedToMe

urlpatterns = [
    path('tasks/', TaskList.as_view(), name='task-list'),
    path('tasks/assigned-to-me/', TasksAssignedToMe.as_view(), name='tasks-assigned'),
]