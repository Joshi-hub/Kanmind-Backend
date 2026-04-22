from django.urls import path, include
from boards_app.api.views import UserBoardListView, BoardListCreateView, BoardRetrieveUpdateDestroyView, BoardListView


urlpatterns = [
    path('boards/', UserBoardListView.as_view(), name='user-boards'),
    path('boards/all/', BoardListCreateView.as_view(), name='all-boards'),
    path('boards/<int:pk>/', BoardRetrieveUpdateDestroyView.as_view(), name='board-detail'),
    path('boards/list/', BoardListView.as_view(), name='board-list'),

]