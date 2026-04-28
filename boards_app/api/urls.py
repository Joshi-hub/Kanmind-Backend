from django.urls import path, include
from boards_app.api.views import BoardListCreateView, BoardRetrieveUpdateDestroyView, EmailCheckView

urlpatterns = [
    path('boards/', BoardListCreateView.as_view(), name='board-list-create'),
    path('boards/<int:pk>/', BoardRetrieveUpdateDestroyView.as_view(), name='board-detail'),
    path('email-check/', EmailCheckView.as_view(), name='email-check'),
]