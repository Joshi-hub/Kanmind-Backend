from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Board
from .serializers import BoardSerializer, BoardPatchSerializer
from user_auth_app.permissions import IsOwnerOrAdmin


class BoardListCreateView(generics.ListCreateAPIView):
    """List all boards for the current user, or create a new board."""

    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return boards where the user is owner or member."""
        user = self.request.user
        return Board.objects.filter(Q(owner=user) | Q(members=user)).distinct()

    def perform_create(self, serializer):
        """Save board with the current user as owner."""
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        """Create a board and set members from the provided ID list."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        members_data = request.data.get('members', [])
        if members_data:
            board = serializer.instance
            board.members.set(User.objects.filter(id__in=members_data))
            board.refresh_from_db()
        return Response(self.get_serializer(serializer.instance).data, status=201)


class BoardRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a single board."""

    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_object(self):
        """Return board or raise 403 if user is not a member or owner."""
        obj = super().get_object()
        if self.request.method in ('GET', 'HEAD', 'OPTIONS'):
            is_owner = obj.owner == self.request.user
            is_member = obj.members.filter(id=self.request.user.id).exists()
            if not (is_owner or is_member):
                raise PermissionDenied('You are not a member of this board.')
        return obj

    def partial_update(self, request, *args, **kwargs):
        """Update board title and/or members list, return owner_data and members_data."""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        members_data = request.data.get('members', None)
        if members_data is not None:
            instance.members.set(User.objects.filter(id__in=members_data))
        instance.refresh_from_db()
        return Response(BoardPatchSerializer(instance).data)


class EmailCheckView(APIView):
    """Check whether a given email address belongs to a registered user."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return user info if the email exists, otherwise 404."""
        email = request.query_params.get('email')
        if not email:
            return Response({'error': 'Email missing'}, status=400)
        try:
            user = User.objects.get(email=email)
            return Response({
                'id': user.id,
                'email': user.email,
                'fullname': f"{user.first_name} {user.last_name}".strip() or user.username,
            }, status=200)
        except User.DoesNotExist:
            return Response({'error': 'Email not found'}, status=404)