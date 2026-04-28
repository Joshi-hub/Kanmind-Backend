from django.shortcuts import render
from rest_framework import generics, serializers
from ..models import Board
from .serializers import BoardSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q, F
from user_auth_app.permissions import IsOwnerOrAdmin
from django.contrib.auth.models import User
from rest_framework.views import APIView


class BoardRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    

class BoardListView(generics.ListAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer   

class BoardListCreateView(generics.ListCreateAPIView):
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(owner=self.request.user) 

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(Q(owner=user) | Q(members=user)).distinct()
        

class UserBoardListView(generics.ListAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(owner=user)
    
class EmailCheckView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        email = request.query_params.get('email')
        if not email:
            return Response({"error": "Email missing"}, status=400)
        
        try:
            user = User.objects.get(email=email)
            return Response({
                "id": user.id,
                "email": user.email,
                "fullname": f"{user.first_name} {user.last_name}".strip() or user.username
            }, status=200)
        except User.DoesNotExist:
            return Response({"error": "Email nicht gefunden"}, status=404)
    
