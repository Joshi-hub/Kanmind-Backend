from django.shortcuts import render
from rest_framework import generics, serializers
from ..models import Board
from .serializers import BoardSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from user_auth_app.permissions import IsOwnerOrAdmin


class BoardRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

class BoardListView(generics.ListAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer   

class BoardListCreateView (generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user) 

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Board.objects.all()
        return Board.objects.filter(owner=self.request.user)
        

class UserBoardListView(generics.ListAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(owner=user)
