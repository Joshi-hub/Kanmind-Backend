from django.urls import path
from .views import (
    TaskListCreateView, 
    TaskDetailView, 
    AssignedToMeTaskListView, 
    ReviewingTaskListView,
    TaskCommentListCreateView
)

urlpatterns = [
    path('', TaskListCreateView.as_view(), name='task-list-create'),
    path('assigned-to-me/', AssignedToMeTaskListView.as_view(), name='tasks-assigned-to-me'),
    path('reviewing/', ReviewingTaskListView.as_view(), name='tasks-reviewing'),
    path('<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('<int:task_id>/comments/', TaskCommentListCreateView.as_view(), name='task-comments'),
]