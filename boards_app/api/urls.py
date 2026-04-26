from django.urls import path, include
from boards_app.api.views import BoardListCreateView, BoardRetrieveUpdateDestroyView


urlpatterns = [
    path('boards/', BoardListCreateView.as_view(), name='board-list-create'),
    path('boards/<int:pk>/', BoardRetrieveUpdateDestroyView.as_view(), name='board-detail'),
]