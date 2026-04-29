from django.shortcuts import render
from rest_framework import generics, serializers
from ..models import Board
from .serializers import BoardSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from user_auth_app.permissions import IsOwnerOrAdmin
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied


class BoardRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_object(self):
        obj = super().get_object()
        if self.request.method in ('GET', 'HEAD', 'OPTIONS'):
            is_owner = obj.owner == self.request.user
            is_member = obj.members.filter(id=self.request.user.id).exists()
            if not (is_owner or is_member):
                raise PermissionDenied("Du bist kein Mitglied dieses Boards.")
        return obj

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        members_data = request.data.get('members', None)
        if members_data is not None:
            members = User.objects.filter(id__in=members_data)
            instance.members.set(members)

        instance.refresh_from_db()
        return Response(self.get_serializer(instance).data)


class BoardListView(generics.ListAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer


class BoardListCreateView(generics.ListCreateAPIView):
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(Q(owner=user) | Q(members=user)).distinct()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        members_data = request.data.get('members', [])
        if members_data:
            board = serializer.instance
            members = User.objects.filter(id__in=members_data)
            board.members.set(members)
            board.refresh_from_db()

        return Response(self.get_serializer(serializer.instance).data, status=201)


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